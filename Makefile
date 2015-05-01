all:
	$(MAKE) -C doc html

check:
	python -m CoverageTestRunner --ignore-missing-from=without-tests
	rm .coverage
	pep8 ttystatus
	if command -v pylint && pylint --version | grep '^pylint [1-9]'; \
        then \
		PYTHONPATH=. pylint --rcfile=pylint.conf ttystatus; \
        fi

clean:
	rm -f .coverage ttystatus/*.py[co]
	rm -rf build
	$(MAKE) -C doc clean
