lint:
		poetry run flake8 --exclude=migrations tasks statuses labels users task_manager
install:
		poetry install

.PHONY: install lint