format:
	poetry run black src tests scripts
	poetry run isort src tests scripts

lint:
	poetry run ruff src tests scripts
	poetry run mypy src

test:
	poetry run pytest

run-pipeline:
	poetry run python scripts/run_preprocessing.py --dataset google --config src/wkr/config/default.yaml
