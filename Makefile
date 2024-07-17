black = black --target-version py312 api
isort = isort --profile black api
flake8 = flake8 --ignore=E203,F401,E402,F841,E501,E722,W503 api

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint:
	mypy --show-error-codes api
	$(flake8)
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: build
build: format
	docker buildx build --no-cache -t visualagents/server:dev  .
