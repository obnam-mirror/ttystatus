all:
	$(MAKE) -C doc html

check:
	python -m CoverageTestRunner --ignore-missing-from=without-tests
	rm .coverage
	
clean:
	rm -f .coverage ttystatus/*.py[co]
	rm -rf build
	$(MAKE) -C doc clean
