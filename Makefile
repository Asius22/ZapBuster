# Makefile for setting up the URL Analyzer project

.PHONY: help install python-deps zap-deps feroxbuster-deps cewl-deps clean

# Default goal
help:
	@echo "Usage:"
	@echo "  make install           Install all dependencies (Python, ZAP, FeroxBuster, CeWL)"
	@echo "  make python-deps       Install Python dependencies"
	@echo "  make zap-deps          Ensure OWASP ZAP is installed"
	@echo "  make feroxbuster-deps  Ensure FeroxBuster is installed"
	@echo "  make cewl-deps         Ensure CeWL is installed"
	@echo "  make clean             Remove Python virtual environment and clean up"



# Install all dependencies
install: update-all python-deps zap-deps feroxbuster-deps cewl-deps
	@echo "All dependencies installed."

update-all:
	@echo "Running update..."
	sudo apt update -y && sudo apt upgrade -y

# Install Python dependencies
python-deps:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Ensure OWASP ZAP is installed
zap-deps:
	@echo "Checking OWASP ZAP..."
	@which zap.sh || (echo "Installing OWASP ZAP..." && sudo apt install zaproxy -y)

# Ensure FeroxBuster is installed
feroxbuster-deps:
	@echo "Checking FeroxBuster..."
	@which feroxbuster || (echo "Installing FeroxBuster..." && sudo apt install feroxbuster -y)

# Ensure CeWL is installed
cewl-deps:
	@echo "Checking CeWL..."
	@which cewl || (echo "Installing CeWL..." && sudo apt install cewl -y)

# Clean up environment
clean:
	@echo "Cleaning up Python environment and temporary files..."
	rm -rf __pycache__
	rm -rf venv
	@echo "Cleanup complete."