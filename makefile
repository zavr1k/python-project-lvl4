lint:
		poetry run python -m flake8 --exclude=migrations tasks users statuses labels
install:
		poetry install

.PHONY: install lint