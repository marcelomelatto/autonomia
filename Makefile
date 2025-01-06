# Caminho para o ambiente virtual
VENV_PATH = .venv
PYTHON = $(VENV_PATH)/bin/python
PIP = $(VENV_PATH)/bin/pip

# Cria o ambiente virtual e instala dependências
.venv:
	python3 -m venv $(VENV_PATH)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Instalar dependências (não há necessidade de repetir a instalação)
install: .venv

# Testes (garante que o ambiente virtual esteja pronto)
test: .venv
	$(PYTHON) -m pytest -vv test_hello.py

# Formatação de código
format: .venv
	$(VENV_PATH)/bin/black 00_autonomia_carga_fria/*.py \
	                       01_autonomia_equipamento/*.py \
	                       02_autonomia_consumo/*.py \
	                       03_autonomia_transito/*.py \
	                       04_autonomia_modelo/*.py

# Linting (garante que o ambiente virtual esteja pronto)
lint: .venv
	$(VENV_PATH)/bin/pylint --disable=R,C hello.py

# Comando geral
all: install lint test