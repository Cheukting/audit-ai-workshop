.PHONY: help install lint format test cov build clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "} {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install:  ## Create the dev environment
	uv sync --all-groups

lint:  ## Run ruff (lint + format check)
	uv run ruff check .
	uv run ruff format --check .

format:  ## Apply ruff formatting and safe fixes
	uv run ruff check --fix .
	uv run ruff format .

test:  ## Run the test suite
	uv run pytest

cov:  ## Run the test suite with coverage
	uv run pytest --cov --cov-report=term-missing

build:  ## Build the sdist and wheel
	uv build

clean:  ## Remove build and cache artefacts
	rm -rf dist build .pytest_cache .ruff_cache .coverage coverage.xml htmlcov
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
