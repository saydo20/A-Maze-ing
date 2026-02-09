PYTHON := python3

MAIN_SCRIPT := mazegen/a_maze_ing.py

CONFIG_FILE := config.txt

install:
	@echo "Installing dependencies..."
	pip install flake8
	pip install build
run:
	@echo "Running the project..."
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)
debug:
	@echo "Running in debug mode..."
	$(PYTHON) -m pdb $(MAIN_SCRIPT)

clean:
	@echo "Cleaning temporary files..."
	rm -rf venv
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	@echo "Running linting..."
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Running strict linting..."
	flake8 .
	mypy . --strict
