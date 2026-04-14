.PHONY: sync
sync:
	uv sync

.PHONY: lint
lint:
	uv run ruff check --exit-zero .

.PHONY: format
format:
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: pre-commit
pre-commit:
	uv run pre-commit run --all-files

.PHONY: lab
lab:
	uv run jupyter lab
