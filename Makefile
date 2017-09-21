.PHONY: test
test:
	py.test test/unittests.py -vv
	py.test --pep8 src/preprocessing.py
	py.test --pep8 src/multicore_processor.py
	py.test --pep8 src/utils.py
