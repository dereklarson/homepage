rm -rf build
mkdir build
cp src/resume.cls build/
python3 src/write_template.py && cd build && xelatex out_template.xtx >> /dev/null && mv out_template.pdf my_resume.pdf
