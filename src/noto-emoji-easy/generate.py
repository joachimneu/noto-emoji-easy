#!/usr/bin/env python3
"""Converts the SVGs in the src/noto-emoji folder to PDF and generates the .ins and .dtx files."""

import json
import os
import shutil
import subprocess
from datetime import date
from operator import itemgetter
from pathlib import Path

import requests
from emoji.unicode_codes import EMOJI_DATA as emoji_db
from jinja2 import Template

VERSION = "1.0"
AUTHOR = "Jost Rossel, Joachim Neu"
NOTO_EMOJI_VERSION = "2.038"

JINJA_SYNTAX = {
    "block_start_string": "<%",
    "block_end_string": "%>",
    "variable_start_string": "<<",
    "variable_end_string": ">>",
    "comment_start_string": "<#",
    "comment_end_string": "#>",
}

script_folder = os.path.dirname(os.path.realpath(__file__))
git_root_dir = os.path.abspath(os.path.join(script_folder, "..", ".."))
source_folder = os.path.join(git_root_dir, "src")
notoemoji_source_folder = os.path.join(source_folder, "noto-emoji")
svg_source_folder = os.path.join(notoemoji_source_folder, "svg")
svg_source_folder2 = os.path.join(notoemoji_source_folder, "third_party", "region-flags", "waved-svg")
target_folder = os.path.join(git_root_dir, "packages")
pdf_temp_folder = os.path.join(git_root_dir, "packages", "pdf-noto-emoji-easy")
all_notoemojieasy_pdf = os.path.join(git_root_dir, "packages", "all-noto-emoji-easy.pdf")

# ensure that all target folders exist and pdf_temp_folder is empty
Path(pdf_temp_folder).mkdir(parents=True, exist_ok=True)
shutil.rmtree(pdf_temp_folder)
Path(pdf_temp_folder).mkdir(parents=True, exist_ok=True)


# add Regional Indicator Symbol Letters A - Z to emoji_db as they are not technically emojis
# but still in the Noto Emoji set and might be useful
for _offset, _letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    emoji_db[chr(127462 + _offset)] = {
        "en": f":Regional Indicator Symbol Letter {_letter}:",
        "status": 2,
        "E": 6,
        "alias": [
            f":regional_indicator_symbol_letter_{_letter.lower()}:",
            f":Letter {_letter}:",
            f":{_letter} Button:",
            f":{_letter}:",
        ],
    }


def get_unicode(filename):
    """Converts the Noto Emoji string file names to their unicode equivalent."""
    assert filename.startswith("emoji_u")
    filename = filename[len("emoji_u"):]
    return "".join([chr(int(uc, 16)) for uc in filename.split("_")])


def _get_alias_data():
    """Searches different sources for natural-language aliases of an emoji."""
    data = {}

    official_names = {}
    emoji_test_file = requests.get(
        "https://unicode.org/Public/emoji/latest/emoji-test.txt"
    ).content.decode("utf-8")
    chars_to_replace = [
        ("“", '"'),
        ("”", '"'),
        ("‘", "'"),
        ("’", "'"),
    ]

    for line in emoji_test_file.split("\n"):
        line = line.strip()
        if line.startswith("#") or len(line) == 0:
            continue

        # a line looks like:
        # 1F600; fully-qualified # 😀 E1.0 grinning face
        _, comment = line.split("#", 1)
        emoji, rest = comment.split("E", 1)
        name = " ".join(rest.split(" ")[1:])
        emoji = emoji.strip()
        name = name.strip()
        for char, replacement in chars_to_replace:
            name = name.replace(char, replacement)

        if emoji in official_names:
            official_names[emoji].append(name)
        else:
            official_names[emoji] = [name]

    data = dict(official_names.items())  # copy official names into data
    used_names = set()  # track used names to avoid duplicates (prio on official names)
    used_names.update(*list(official_names.values()))

    def _add_alias(emoji, alias):
        if alias in used_names:
            return
        if emoji in data:
            data[emoji].append(alias)
        else:
            data[emoji] = [alias]
        used_names.add(alias)

    for emoji, emoji_data in emoji_db.items():
        _add_alias(emoji, emoji_data["en"][1:-1])
        for alias in emoji_data.get("alias", []):
            _add_alias(emoji, alias[1:-1])

    return data


def convert_svg_to_pdf():
    """Converts the SVG files to PDF using inkscape.
    Returns all filenames, their list index corresponds to the page in the PDF (+1)."""
    names = set()
    inkscape_call = []

    targets = set()
    for _filename in os.listdir(svg_source_folder):
        if _filename[-4:] != ".svg":
            continue
        names.add(_filename[:-4])
        tar = f"{os.path.join(pdf_temp_folder, _filename[:-4])}.pdf"
        inkscape_call.append(
            f"file-open:{os.path.join(svg_source_folder, _filename)};"
            "export-type:pdf;"
            f"export-filename:{tar};"
            "export-do;"
        )
        targets.add(tar)
    inkscape_call.append("\n")

    subprocess.run(
        ["inkscape", "--shell"],
        input="".join(inkscape_call).encode("utf-8"),
        check=True,
    )

    # verify generation
    for tar in targets:
        if not os.path.isfile(tar):
            print("Missing", tar)

    names = sorted(names)
    sorted_targets = [f"{os.path.join(pdf_temp_folder, name)}.pdf" for name in names]

    subprocess.run(
        ["pdfunite", *sorted_targets, all_notoemojieasy_pdf],
        check=True,
    )

    return names


def get_metadata():
    """Retrieves the needed metadata for the templates."""
    metadata = {}
    metadata["original_version"] = NOTO_EMOJI_VERSION
    metadata["year"] = date.today().year
    metadata["month"] = date.today().month
    metadata["day"] = date.today().day
    metadata["version"] = VERSION
    metadata["author"] = AUTHOR
    return metadata


if __name__ == "__main__":
    emoji_aliases = _get_alias_data()
    filenames = convert_svg_to_pdf()

    context = get_metadata()

    context["emojinames"] = []
    context["emojinames_mapping"] = {}
    
    for index, unicode in enumerate(filenames):
        page = index + 1
        unicode_raw = unicode
        assert unicode.startswith("emoji_u")
        unicode = unicode[len("emoji_u"):].replace("_", "-")
        aliases = [unicode]
        if get_unicode(unicode_raw) in emoji_aliases:
            aliases.extend(emoji_aliases[get_unicode(unicode_raw)])
        if len(aliases) == 1:
            continue
        context["emojinames_mapping"][unicode] = aliases
        for alias in aliases:
            context["emojinames"].append((page, alias))

    context["emojinames"].sort(key=itemgetter(0, 1))
    context["emojinames_mapping"] = sorted(context["emojinames_mapping"].items())

    with open(os.path.join(git_root_dir, "src", "licenses.tex"), encoding="utf-8") as f:
        context["license_text"] = f.read().split("\n")

    with open(os.path.join(target_folder, "noto-emoji-easy.ins"), "w", encoding="utf-8") as outfile:
        ins_template = Template(
            open(os.path.join(script_folder, "ins.jinja"), encoding="utf-8").read(), **JINJA_SYNTAX
        )
        outfile.write(ins_template.render(context))

    with open(os.path.join(target_folder, "noto-emoji-easy.dtx"), "w", encoding="utf-8") as outfile:
        dtx_template = Template(
            open(os.path.join(script_folder, "dtx.jinja"), encoding="utf-8").read(), **JINJA_SYNTAX
        )
        outfile.write(dtx_template.render(context))
