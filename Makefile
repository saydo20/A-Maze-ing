PYTHON := python3

MAIN_SCRIPT := a_maze_ing.py

CONFIG_FILE := config.txt

install:
	@echo "Installing dependencies..."
	pip install flake8
	pip install mypy
	pip install build
run:
	@echo "Running thee project..."
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)
	
debug:
	@echo "Running in debug mode..."
	$(PYTHON) -m pdb $(MAIN_SCRIPT)

clean:
	@echo "Cleaning temporary files..."
	rm -rf dist
	rm -rf build
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf */__pycache__
	rm -f *.pyc

lint:
	@echo "Running linting..."
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
