#!/bin/sh

echo "Running conversion to xml..."
echo "LATEX_DIR = ${LATEX_DIR}"
echo "TEX_FILENAME = ${TEX_FILENAME}"
echo "BIB_FILENAME = ${BIB_FILENAME}"

docker_latex_dir="/data/${LATEX_DIR}"

cp /tmp/tex2xml.sh "$docker_latex_dir/"
cp /tmp/apa.csl "$docker_latex_dir/"
cp /tmp/cleanjats.py "$docker_latex_dir/"
cd "$docker_latex_dir"

sh ./tex2xml.sh "$TEX_FILENAME" "$BIB_FILENAME"

echo "Conversion to xml completed."

exec "$@"