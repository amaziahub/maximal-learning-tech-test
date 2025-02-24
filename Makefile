.PHONY: all


test:
	@echo "Running tests..."
	venv/bin/python -m pytest

install:
	@echo "Installing dependencies..."
	venv/bin/python -m pip install -r requirements.txt
