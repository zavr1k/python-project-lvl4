lint:
		poetry run python -m flake8 --exclude=migrations tasks users statuses
install:
		poetry install

.PHONY: install lint