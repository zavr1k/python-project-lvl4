lint:
		poetry run python -m flake8 --exclude=migrations tasks
install:
		poetry install

.PHONY: install lint