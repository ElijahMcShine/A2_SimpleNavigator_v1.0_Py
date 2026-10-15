SHELL = /bin/sh
PYTHON = python3

#Intall dir.
EXEC_PREFIX = ../ap2-navigator
TEST_EXEC_PREFIX = ../test

SRC_TEXI = ./dvi.texi

#Distribution variables
PORTNAME = ap2-navigator
PORTVERSION = 0.0.9
DISTNAME = $(PORTNAME)_$(PORTVERSION)-stilwool-suannefu
DISTFILES = package_algorithms package_cli package_graph tests app.py requirements.txt dvi.texi Makefile


all: install

install: clean create_dir s21_graph s21_graph_algorithms s21_navigator_cli
	cp app.py $(EXEC_PREFIX)
	cp requirements.txt $(EXEC_PREFIX)
	$(PYTHON) -m venv $(EXEC_PREFIX)/venv
	$(EXEC_PREFIX)/venv/bin/pip install --find-links=$(EXEC_PREFIX)/ -r $(EXEC_PREFIX)/requirements.txt
	
s21_graph: package_graph create_dir
	rm -rf ./package_graph/venv
	rm -rf ./package_graph/dist
	$(PYTHON) -m venv ./package_graph/venv
	./package_graph/venv/bin/pip install build
	./package_graph/venv/bin/$(PYTHON) -m build ./package_graph
	cp ./package_graph/dist/s21_graph*.whl $(EXEC_PREFIX)
	rm -rf ./package_graph/venv
	rm -rf ./package_graph/dist

s21_graph_algorithms: package_algorithms create_dir
	rm -rf ./package_algorithms/venv
	rm -rf ./package_algorithms/dist
	$(PYTHON) -m venv ./package_algorithms/venv
	./package_algorithms/venv/bin/pip install build
	./package_algorithms/venv/bin/$(PYTHON) -m build ./package_algorithms
	cp ./package_algorithms/dist/s21_graph_algorithms*.whl $(EXEC_PREFIX)
	rm -rf ./package_algorithms/venv
	rm -rf ./package_algorithms/dist

s21_navigator_cli: package_cli create_dir
	rm -rf ./package_cli/venv
	rm -rf ./package_cli/dist
	$(PYTHON) -m venv ./package_cli/venv
	./package_cli/venv/bin/pip install build
	./package_cli/venv/bin/$(PYTHON) -m build ./package_cli
	cp ./package_cli/dist/s21_navigator_cli*.whl $(EXEC_PREFIX)
	rm -rf ./package_cli/venv
	rm -rf ./package_cli/dist

create_dir:
	[ -d $(EXEC_PREFIX) ] || mkdir $(EXEC_PREFIX)

install_run: install
	$(EXEC_PREFIX)/venv/bin/$(PYTHON) $(EXEC_PREFIX)/app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -rf {} +
	rm -rf venv
	rm -rf .coverage
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

uninstall:
	rm -rf $(EXEC_PREFIX)

build_test: clean package_cli package_algorithms package_graph
	[ -d $(TEST_EXEC_PREFIX) ] || mkdir $(TEST_EXEC_PREFIX)
	cp -r ./package_graph/s21_graph $(TEST_EXEC_PREFIX)
	cp -r ./package_algorithms/s21_graph_algorithms $(TEST_EXEC_PREFIX)
	cp -r ./package_cli/s21_navigator_cli $(TEST_EXEC_PREFIX)
	cp -r ./tests $(TEST_EXEC_PREFIX)
	cp app.py $(TEST_EXEC_PREFIX)/
	$(PYTHON) -m venv $(TEST_EXEC_PREFIX)/venv
	$(TEST_EXEC_PREFIX)/venv/bin/pip install -r $(TEST_EXEC_PREFIX)/s21_graph/requirements.txt
	$(TEST_EXEC_PREFIX)/venv/bin/pip install -r $(TEST_EXEC_PREFIX)/s21_graph_algorithms/requirements.txt
	$(TEST_EXEC_PREFIX)/venv/bin/pip install pytest

test: build_test
	PYTHONPATH=./ $(TEST_EXEC_PREFIX)/venv/bin/pytest $(TEST_EXEC_PREFIX)/tests/
	rm -rf $(TEST_EXEC_PREFIX)
	make clean

gcov_report: build_test
	rm -rf htmlcov
	$(TEST_EXEC_PREFIX)/venv/bin/pip install pytest-cov
	PYTHONPATH=./ $(TEST_EXEC_PREFIX)/venv/bin/pytest $(TEST_EXEC_PREFIX)/tests/ -p pytest_cov --cov=$(TEST_EXEC_PREFIX)/. --cov-report=html --cov-fail-under=60
	rm -rf $(TEST_EXEC_PREFIX)
	make clean

gcov_report_open: gcov_report
	open htmlcov/index.html

dist: 
	[ -d $(DISTNAME) ] || mkdir $(DISTNAME)
	$(foreach var,$(DISTFILES), cp -R $(var) $(DISTNAME);)
	tar -czvf $(DISTNAME).tar.gz $(DISTNAME)
	rm -rf $(DISTNAME)


.PHONY: test gcov_report dist