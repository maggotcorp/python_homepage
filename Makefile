.PHONY: all lint clean build run kill help

# Configuration
PORT ?= 5000

all: lint build run

lint:
	pip install pylint --break-system-packages
	pylint src/app.py

clean: kill
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

build: kill
	pip install -r requirements.txt --break-system-packages

run:
	python src/app.py --port $(PORT)

kill:
	@echo "Killing any running Flask application instances..."
	-pkill -f "python src/app.py" 2>/dev/null || true
	-pkill -f "python.*app.py" 2>/dev/null || true
	-pkill -f "flask" 2>/dev/null || true
	-pkill -f "python.*5000" 2>/dev/null || true
	-pkill -f "python.*8009" 2>/dev/null || true
	-pkill -f "python.*8080" 2>/dev/null || true
	@echo "Done."

help:
	@echo "Available targets:"
	@echo "  all    - Run lint, build, and run in sequence"
	@echo "  lint   - Install and run pylint on src/app.py"
	@echo "  clean  - Kill running instances and remove .pyc files"
	@echo "  build  - Kill running instances and install dependencies"
	@echo "  run    - Run the application on port $(PORT)"
	@echo "  kill   - Kill any running Flask application instances"
	@echo "  help   - Show this help message"
	@echo ""
	@echo "Configuration:"
	@echo "  PORT   - Port number for the application (default: 5000)"
	@echo "           Usage: make run PORT=8080"