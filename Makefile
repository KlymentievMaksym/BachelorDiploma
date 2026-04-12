# Змінні
PYTHON = python
VENV = .venv
BIN = $(VENV)/Scripts

.PHONY: setup update clean

setup: $(VENV)/bin/activate

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python.exe -m pip install --upgrade pip
	$(BIN)/pip install -e ./colorization-engine
	$(BIN)/pip install -r ./colorization-app/requirements.txt

update:
	git submodule update --init --recursive
	git submodule foreach git pull origin main

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +