lint:
		poetry run python -m flake8 --exclude=migrations tasks users
install:
		poetry install

.PHONY: install lint