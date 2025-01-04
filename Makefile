# Caminho para o ambiente virtual
VENV_PATH = .venv

# Cria o ambiente virtual
.venv:
	python3 -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/pip install --upgrade pip
	$(VENV_PATH)/bin/pip install -r requirements.txt

# Instalar dependências
install: .venv
	$(VENV_PATH)/bin/pip install --upgrade pip
	$(VENV_PATH)/bin/pip install -r requirements.txt

# Testes
test: .venv
	$(VENV_PATH)/bin/python -m pytest -vv test_hello.py

# Formatação de código
format: .venv
	$(VENV_PATH)/bin/black 00_autonomia_carga_fria/*.py
	$(VENV_PATH)/bin/black 01_autonomia_equipamento/*.py
	$(VENV_PATH)/bin/black 02_autonomia_consumo/*.py
	$(VENV_PATH)/bin/black 03_autonomia_transito/*.py
	$(VENV_PATH)/bin/black 04_autonomia_modelo/*.py

# Linting
lint: .venv
	$(VENV_PATH)/bin/pylint --disable=R,C hello.py

# Comando geral
all: install lint test
