all:

check:
	python -m CoverageTestRunner --ignore-missing-from=without-tests
	rm .coverage
	
clean:
	rm -f .coverage ttystatus/*.py[co]
