.PHONY: test upload clean bootstrap

test:
	sh -c '. _virtualenv/bin/activate; nosetests tests'

test-all:
	tox

build-test:
	make package
	make upload-test

venv-test:
	make venv-clean
	make venv2
	make venv3

package:
	python3 setup.py sdist

venv3:
	virtualenv --python=python3 .venv-testing-3
	.venv-testing-3/bin/pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pytle

venv2:
	virtualenv --python=python2 .venv-testing-2
	.venv-testing-2/bin/pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pytle

venv-clean:
	rm -rf .venv-testing-3
	rm -rf .venv-testing-2

upload-test:
	twine upload --repository testpypi dist/*

upload-prod:
	twine upload dist/*
    
register:
	python setup.py register

clean:
	rm -f MANIFEST
	rm -rf build dist

bootstrap:
	virtualenv --python=python$(pyv) .venv$(pyv)
	.venv$(pyv)/bin/pip install --upgrade pip
	.venv$(pyv)/bin/pip install --upgrade setuptools
ifneq ($(wildcard requirements.txt),) 
	.venv$(pyv)/bin/pip install -r requirements.txt
endif

# Version Up
# git add
# git commit
# git push
# make build-test
# make venv-test
#    test
# make upload-prod