.PHONY: all test install clean-pyc clean-build

all:
	@echo "install"
	@echo "test"
	@echo "clean"

install: clean
	pip install -e . -r requirements-test.txt

uninstall: clean
	pip uninstall -y -r requirements.txt -r requirements-test.txt

test: 
	coverage run --source daedalus -m py.test -l
	@coverage report

coverage: test
	@coverage html
	@echo "open htmlcov/index.html"

clean: clean-build clean-pyc

clean-build:
	@rm -fr *.egg-info
	@rm -fr htmlcov/

clean-pyc:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
