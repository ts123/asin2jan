
all: test
test:
	./asin2jan.py B005119CMA
clean:
	find . ! -path './.git*' ! -name '*.md' ! -name Makefile ! -name '*.py' -delete
install:
	pip install -e . -v --user 
uninstall:
	pip uninstall asin2jan -v -y

