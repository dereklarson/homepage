rm -rf build
mkdir build
python3 src/write_template.py && \
	cd build && \
	echo "Compiling dark-theme resume" && \
	xelatex template_output.xtx >> /dev/null && \
       	mv template_output.pdf my_resume.pdf && \
	cp my_resume.pdf ../../static/resume.pdf && \
	cp light_resume.cls resume.cls && \
	echo "Compiling light-theme resume" && \
	xelatex template_output.xtx >> /dev/null && \
       	mv template_output.pdf printable_resume.pdf && \
	cp printable_resume.pdf ../../static/printable_resume.pdf
