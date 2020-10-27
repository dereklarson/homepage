rm -rf build
mkdir build
python3 src/write_template.py && \
	cd build && \
	xelatex template_output.xtx && \
       	mv template_output.pdf my_resume.pdf
