# Noto Emojis

Simple wrapper that allows to use Google's Noto Emoji emojis through LaTeX commands.
As this package works with graphics and not with fonts to achieve its goal, it *should* work on every machine with any LaTeX version without problems.

In comparison, the `emoji` package on CTAN <https://www.ctan.org/pkg/emoji> works on fonts and requires `lualatex`.
It is lighter and probably compiles faster if you use thousands of emojis, but it also has stricter requirements and is not as flexible.

This package really is intended to be used within Ti*k*Z images.

## Usage

This package in on [CTAN](https://www.ctan.org) as [noto-emoji-easy](https://ctan.org/pkg/noto-emoji-easy), so you should be able to use it like any other package, with

```latex
\usepackage{noto-emoji-easy}
```

An emoji can be used via `\notoemoji{...}`.
There is the alternative `\textnotoemoji{...}` command which scales and sets the emoji to fit the text line.
More information can be found in the [package's documentation](https://ftp.gwdg.de/pub/ctan/macros/latex/contrib/noto-emoji-easy/noto-emoji-easy.pdf).

## Installation

If the package is not in you TeX distribution, try [these install steps](https://tex.stackexchange.com/questions/73016/how-do-i-install-an-individual-package-on-a-linux-system).
The TL;DR for the manual installation (if everything else fails) is:
- Build the package from the repository, so that the `dist` and `packages` folders are populated (not included in the repo).
- Run `kpsewhich -var-value TEXMFLOCAL` and `kpsewhich -var-value TEXMFHOME` and check which of the resulting directories is populated.
  Lets call the resulting directory `<base dir>`.
- Create the directory `<base dir>/tex/latex/noto-emoji-easy` and copy the files `noto-emoji-easy.sty` and `all-noto-emoji-easy.pdf` from `packages` there.
- Run `mktexlsr` (you probably need root for that).
- If something doesn't work, read the long version linked above (Method 3).

## Problems/TODOs

- Currently the emojis are not text-selectable, that might change in future versions.

# Implementation Notice

As the emojis are PDF-based and use transparency, they include groups.
I was not able to change the `inkscape` export so that that does not happen.
Hence, `pdflatex` throws a warning about multiple groups on one PDF page.
This package disables said warning: `\pdfsuppresswarningpagegroup=1` as it is of no concern for the inputted emojis.
It **could** happen, that a PDF you input is faulty and you don't notice due to said suppression.
You can enable the warning with `\pdfsuppresswarningpagegroup=0`.
