IGNORED_FILES := 00_autonomia_carga_fria/01_extract.py

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_hello.py
	python -m pytest -vv $(filter-out $(IGNORED_FILES), 00_autonomia_carga_fria/04_test.py)

format:
	black $(filter-out $(IGNORED_FILES), 00_autonomia_carga_fria/*.py)
	black 01_autonomia_equipamento/*.py
	black 02_autonomia_consumo/*.py
	black 03_autonomia_transito/*.py
	black 04_autonomia_modelo/*.py

lint:
	pylint --disable=R,C hello.py

all: install lint test
