ANTLR = java -jar antlr-4.7.1-complete.jar

run: code
	python execute.py

test: code
	python printtree.py

code: macros.g4
	$(ANTLR) -Dlanguage=Python2 macros.g4

clean:
	\rm -rf
