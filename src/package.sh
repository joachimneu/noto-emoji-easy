#!/bin/bash -ve

# assumes the name of the package (folder name in src and packages) as the first parameter $1

FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

SRC_DIR="${FILE_DIR}/$1"
PKG_DIR="${FILE_DIR}/../packages"
DST_DIR="${FILE_DIR}/../dist/$1"

# cleanup
rm -rf "${DST_DIR}"
mkdir -p "${DST_DIR}"

cd "${PKG_DIR}" || exit
pdflatex -interaction batchmode "$1.ins" || exit
pdflatex -interaction batchmode "$1.dtx" || exit
pdflatex -interaction batchmode "$1.dtx" || exit
if [ "$1" = "noto-emoji-easy" ]; then
    cp "all-noto-emoji-easy.pdf" "${DST_DIR}"
fi
cp "$1.dtx" "${DST_DIR}"
cp "$1.ins" "${DST_DIR}"
cp "$1.pdf" "${DST_DIR}"

cd "${SRC_DIR}" || exit
cp "README.md" "${DST_DIR}"
printf "\n" >> "${DST_DIR}/README.md"
cat "${FILE_DIR}/licenses.md" >> "${DST_DIR}/README.md"

cd "${DST_DIR}/.." || exit
zip -q -r "$1" "$1"
