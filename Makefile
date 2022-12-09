# Development:
# Test repository code:
#
# Test a single version of Python and Matplotlib; install anaconda3 & create env if needed.
#   make repository-test-single PYTHON=3.8 MATPLOTLIB=3.6 
#
# Run tests that require visual inspection
#   make repository-test-single-visual PYTHON=3.8 MATPLOTLIB=3.6 
#
# Test a single version of Python and all values of Matplotlib; create conda env if needed.
#   make repository-test PYTHON=3.8
#
# Remove ./anaconda3 and run all tests (all combos of Python/Matplotlib)
#   make repository-test-all
#
# Making a local package:
# 1. Update CHANGES.txt to have a new version line
# 2. make package-test PYTHON=3.8 MATPLOTLIB=3.5 # (Probably don't need to test all combos)
#
# Test https://colab.research.google.com/github/hapi-server/client-python-notebooks/blob/master/hapi_demo.ipynb#examples
#
#
# Upload package to pypi.org test starting with uploaded package:
# 1. make release
# 2. Wait ~5 minutes and execute
# 3. make release-test-all
#    (Will fail until new version is available at pypi.org for pip install.
#     Sometimes takes ~5 minutes even though web page is immediately
#     updated.)
# 4. After package is finalized, create new version number in CHANGES.txt ending
#    with "b0" in setup.py and then run
#       make version-update
# 	git commit -a -m "Update version for next release"
#    This will update the version information in the repository to indicate it
#    is now in a pre-release state.

# https://matplotlib.org/stable/devel/min_dep_policy.html
ifeq ($(PYTHON),3.5)
	MATPLOTLIBS=3.0
endif

ifeq ($(PYTHON),3.6)
	MATPLOTLIBS=3.2 3.1 3.0
endif

ifeq ($(PYTHON),3.7)
	MATPLOTLIBS=3.5 3.4 3.3 3.2 3.1 3.0
endif

ifeq ($(PYTHON),3.8)
	# 3.0 fails on OS-X with 
	# "The C/C++ header for freetype2 (ft2build.h)
	# could not be found.  You may need to install the
	# development package.""
	MATPLOTLIBS=3.6 3.5 3.4 3.3 3.2 3.1
endif

ifeq ($(PYTHON),3.9)
	# 3.0-3.3 fail on OS-X with error: fatal error: 'ft2build.h' file not found
	MATPLOTLIBS=3.6 3.5 3.4
endif

# Python versions to test
PYTHONS=3.9 3.8 3.7 3.6 3.5

# VERSION is updated in "make version-update" step and derived
# from CHANGES.txt. Do not edit.
VERSION=0.2.3b0
SHELL:= /bin/bash

LONG_TESTS=false

# Location to install Anaconda. Important: This directory is removed when
# make test is executed.
CONDA=./anaconda3

# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
  # CONDA=/c/tools/anaconda3
	CONDA=/c/tools/miniconda3
endif

CONDA_ACTIVATE=source $(CONDA)/etc/profile.d/conda.sh; conda activate

# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
	CONDA_ACTIVATE=source $(CONDA)/Scripts/activate; conda activate
endif

URL=https://upload.pypi.org/
REP=pypi

pythonw=python$(PYTHON)
# ifeq ($(shell uname -s),MINGW64_NT-10.0-18362)
ifeq ($(TRAVIS_OS_NAME),windows)
	pythonw=python
endif
ifeq ($(UNAME_S),Darwin)
	# Use pythonw instead of python. On OS-X, this prevents "need to install
	# python as a framework" error. The following finds the path to the binary
	# of $(PYTHON) and replaces it with pythonw, e.g., 
	# /opt/anaconda3/envs/python3.6/bin/python3.6
	# -> 
	# /opt/anaconda3/envs/python3.6/bin/pythonw
	#a=$(shell source activate python-$(PYTHON)-matplotlib-$(MATPLOTLIB); which python$(PYTHON))
	#pythonw=$(subst bin/python$(PYTHON),bin/pythonw,$(a))
endif

################################################################################
# Test contents in repository using different python versions
test:
	make repository-test-all

repository-test-all:
	- rm -rf $(CONDA)
	@ for version in $(PYTHONS) ; do \
		make repository-test PYTHON=$$version ; \
	done

repository-test:
	$(foreach MATPLOTLIB, $(MATPLOTLIBS), \
		make repository-test-single MATPLOTLIB=$(MATPLOTLIB) PYTHON=$(PYTHON); )

repository-test-single:
	make anaconda3/envs/python-$(PYTHON)-matplotlib-$(MATPLOTLIB) MATPLOTLIB=$(MATPLOTLIB) PYTHON=$(PYTHON)
	$(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB) && python$(PYTHON) -m pytest -rx -rP -v test/test_hapiplot.py

# These require visual inspection.
repository-test-single-visual:
	# Run using pythonw instead of python only so plot windows always work
	# for programs called from command line. This is needed for (at least)
	# OS-X, Python 3.5, and matplotlib instaled from pip.
	make anaconda3/envs/python-$(PYTHON)-matplotlib-$(MATPLOTLIB) MATPLOTLIB=$(MATPLOTLIB) PYTHON=$(PYTHON)
	$(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB); $(pythonw) hapiplot_demo.py
	$(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB); $(pythonw) test/test_hapiplot_visual.py
	#jupyter-notebook ../client-python-notebooks/hapi_demo.ipynb
################################################################################

################################################################################
# Anaconda
CONDA_PKG=Miniconda3-latest-Linux-x86_64.sh
ifeq ($(shell uname -s),Darwin)
	CONDA_PKG=Miniconda3-latest-MacOSX-x86_64.sh
endif

anaconda3/envs/python-$(PYTHON)-matplotlib-$(MATPLOTLIB): anaconda3
ifeq ($(TRAVIS_OS_NAME),windows)
	cp $(CONDA)/Library/bin/libcrypto-1_1-x64.* $(CONDA)/DLLs/
	cp $(CONDA)/Library/bin/libssl-1_1-x64.* $(CONDA)/DLLs/
	$(CONDA)/Scripts/conda create -y --name python-$(PYTHON)-matplotlib-$(MATPLOTLIB) python=$(PYTHON)
else
	$(CONDA_ACTIVATE); \
		$(CONDA)/bin/conda create -y --name python-$(PYTHON)-matplotlib-$(MATPLOTLIB) python=$(PYTHON)
endif
	$(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB) && pip install matplotlib=="$(MATPLOTLIB).*"
	@ $(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB) && python$(PYTHON) setup.py develop | grep "Best"
	# Not sure why the install of pytest is needed given it is in setup.py, but I get pytest install errors otherwise.
	# Note that pillow==8 is needed for Python 3.6. Ideally this would be set in setup.py.
	#@ $(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB) && pip install pytest; pip install .

anaconda3: /tmp/$(CONDA_PKG)
	test -d anaconda3 || bash /tmp/$(CONDA_PKG) -b -p $(CONDA)

/tmp/$(CONDA_PKG):
	curl https://repo.anaconda.com/miniconda/$(CONDA_PKG) > /tmp/$(CONDA_PKG) 
################################################################################

################################################################################
venv-test:
	cp hapiplot_demo.py /tmp # TODO: Explain why needed.
	source env-$(PYTHON)/bin/activate && \
	  pip install pytest ipython && \
		pip uninstall -y hapiplot && \
		pip install --pre '$(PACKAGE)' \
			--index-url $(URL)/simple  \
			--extra-index-url https://pypi.org/simple && \
		env-$(PYTHON)/bin/pytest -v test/test_hapiplot.py && \
		env-$(PYTHON)/bin/ipython /tmp/hapiplot_demo.py
################################################################################

################################################################################
# Packaging
package:
	make clean
	make version-update
	python setup.py sdist

env-$(PYTHON):
	$(CONDA_ACTIVATE) python-$(PYTHON)-matplotlib-$(MATPLOTLIB); \
		conda install -y virtualenv; \
		python$(PYTHON) -m virtualenv env-$(PYTHON)

package-test:
	make package
	make env-$(PYTHON)
	make venv-test PACKAGE='dist/hapiplot-$(VERSION).tar.gz'
################################################################################

################################################################################
release:
	make package
	make version-tag
	make release-upload

release-upload:
	pip install twine
	echo "rweigel, t1p"
	twine upload \
		-r $(REP) dist/hapiplot-$(VERSION).tar.gz \
		&& echo Uploaded to $(subst upload.,,$(URL))/project/hapiplot/

release-test-all:
	@ for version in $(PYTHONS) ; do \
		make release-test PYTHON=$$version ; \
	done

release-test:
	rm -rf env
	$(CONDA_ACTIVATE) $(PYTHON)-matplotlib-$(MATPLOTLIB); pip install virtualenv; python$(PYTHON) -m virtualenv env
	make venv-test PACKAGE='hapiplot==$(VERSION)'
################################################################################

################################################################################
# Update version based on content of CHANGES.txt
version-update:
	python misc/version.py

version-tag:
	- git commit -a -m "Last $(VERSION) commit"
	- git push
	git tag -a v$(VERSION) -m "Version "$(VERSION)
	git push --tags
################################################################################

################################################################################
# Install package in local directory (symlinks made to local dir)
install-local:
	#python setup.py -e .
	$(CONDA_ACTIVATE) $(PYTHON)-matplotlib-$(MATPLOTLIB); pip install --editable .

install:
	pip install 'hapiplot==$(VERSION)' --index-url $(URL)/simple
	conda list | grep hapiplot
	pip list | grep hapiplot
################################################################################

clean:
	- @find . -name __pycache__ | xargs rm -rf {}
	- @find . -name *.pyc | xargs rm -rf {}
	- @find . -name *.DS_Store | xargs rm -rf {}
	- @find . -type d -name __pycache__ | xargs rm -rf {}
	- @find . -name *.pyc | xargs rm -rf {}
	- @rm -f *~
	- @rm -f \#*\#
	- @rm -rf env
	- @rm -rf dist
	- @rm -f MANIFEST
	- @rm -rf .pytest_cache/
	- @rm -rf hapiplot.egg-info/
	- @rm -rf /c/tools/Anaconda3/envs/python3.6/Scripts/wheel.exe*
	- @rm -rf /c/tools/Anaconda3/envs/python3.6/vcruntime140.dll.*
