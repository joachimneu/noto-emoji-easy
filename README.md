# LaTeX Noto Emoji Font

This repository contains the LaTeX package [`noto-emoji-easy`](src/noto-emoji-easy) that is a simple wrapper to use [Google's Noto Emoji](https://github.com/googlefonts/noto-emoji) through LaTeX commands. As this package is not based on fonts, but on `includegraphics`, it supports `pdflatex`, and is particularly useful in Ti*k*Z images.

**This repository is a port of Jost Rossel's excellent [`twemojis`](https://gitlab.com/rossel.jost/latex-twemojis) package from Twitter's Twemojis to Google's Noto Emojis.**

# Development

## Building

To build the package, you need `python3` and a PDF-capable LaTeX installation (`pdflatex`, `lualatex`, ...).
You also need `inkscape` and `pdfunite` (poppler), and the official [`noto-emoji`](https://github.com/googlefonts/noto-emoji) and [`emoji-metadata`](https://github.com/googlefonts/emoji-metadata) repos (init the submodules).

This project uses [poetry](https://python-poetry.org/), so either use that or install the packages from the `pyproject.toml` manually.

To create the ZIP file that will eventually hopefully be uploaded to CTAN, simply run `make <project-name>`.
The resulting ZIP is in the `./dist` folder, the contents of the ZIP files are in sibling-folders.
The `.sty` and compiled documentation can be found in `./packages`.
Both `./dist` and `./packages` are ignored by Git.

# Licenses

**I am not a lawyer, so take this section with a grain of salt, and do your own research!**

## Emojis

Most of the Noto Emoji image resources are under the Apache license, version 2.0:
https://github.com/googlefonts/noto-emoji/blob/main/LICENSE
https://github.com/googlefonts/noto-emoji/blob/main/svg/LICENSE

Most flag images are in the public domain or otherwise exempt from copyright:
https://github.com/googlefonts/noto-emoji/blob/main/third_party/region-flags/LICENSE

For details, see the Noto Emoji repo:
https://github.com/googlefonts/noto-emoji

## LaTeX Package

The LaTeX package is licensed under the LPPL 1.3 or later License.

> Copyright (c) 2021-2022 Jost Rossel, 2023 Joachim Neu
>
> This file may be distributed and/or modified under the
> conditions of the LaTeX Project Public License, either
> version 1.3 of this license or (at your option) any later
> version. The latest version of this license is in:
>
>     http://www.latex-project.org/lppl.txt
>
> and version 1.3 or later is part of all distributions of
> LaTeX version 2005/12/01 or later.

## Python Code

The Python code that generates the LaTeX packages is licensed under the MIT License.

> Copyright (c) 2021-2022 Jost Rossel, 2023 Joachim Neu
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
