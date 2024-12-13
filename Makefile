SHELL=/bin/bash

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans


install:
	@echo "Instalando dependencias localmente"
	@( \
		if [ ! -d .venv ]; then echo""; echo "Virtualenv"; virtualenv -p python3 .venv; fi; \
		source .venv/bin/activate; \
		echo ""; echo "Requirements"; pip install -qU pip; \
		pip install --upgrade -r requirements.txt; \
		echo""; echo "Hooks"; cd .git/hooks; \
		ln -sf ../../git_hooks/pre-commit ./pre-commit; \
		ln -sf ../../git_hooks/pre-push ./pre-push; \
		cd ..; \
	)

build:
	@echo "Construyendo imagen"
	@( \
		docker login; \
		docker build -t $${ALEJANDRIA_IMAGE}:$${CI_COMMIT_SHORT_SHA} . --no-cache; \
		docker push $${ALEJANDRIA_IMAGE}:$${CI_COMMIT_SHORT_SHA}; \
		docker tag $${ALEJANDRIA_IMAGE}:$${CI_COMMIT_SHORT_SHA} $${ALEJANDRIA_IMAGE}:$${TAG_IMAGE}; \
		docker push $${ALEJANDRIA_IMAGE}:$${TAG_IMAGE}; \
	)


deploy:
	@echo "Deploy imagen"
	@( \
		docker pull $${ALEJANDRIA_IMAGE}:$${CI_COMMIT_SHORT_SHA}; \
		docker-compose up -d --no-build; \
		docker rmi -f  $$(docker images $${ALEJANDRIA_IMAGE}*  -f before=$${ALEJANDRIA_IMAGE}:$${CI_COMMIT_SHORT_SHA} -q) \
	)


test-end2end:
	@(	\
		source .venv/bin/activate; \
		export FLASK_ENV=test; \
		pytest -s `find tests -iname 'end2end'`; \
	)

test-integration:
	@(	\
		source .venv/bin/activate; \
		export FLASK_ENV=test; \
		pytest -s `find tests -iname 'integration'`; \
	)

test-unit:
	@(	\
		source .venv/bin/activate; \
		export FLASK_ENV=test; \
		pytest -s `find tests -iname 'unit'`; \
	)

test:
	@(	\
		docker-compose -f docker-compose-test.yaml build; \
		docker-compose -f docker-compose-test.yaml run --rm alejandria make test-all; \
		docker-compose -f docker-compose-test.yaml down --remove-orphans; \
	)

test-all:
	@(	\
		export FLASK_ENV=test; \
		pytest --cov-report xml --cov-report term  `find tests -iname 'unit'` `find tests -iname 'integration'` `find tests -iname 'end2end'` tests/; \
	)

test-file:
	@(	\
		source .venv/bin/activate; \
		export FLASK_ENV=test; \
		pytest --cov-report xml --cov-report term --cov=. $(file); \
	)


up-local:
	@(	\
		source .venv/bin/activate; \
		export FLASK_ENV=development; \
		flask --app app --debug  run --host=0.0.0.0; \
	)

shell:
	@(	\
		source .venv/bin/activate; \
		export FLASK_ENV=development; \
		flask --app app --debug shell; \
	)

black:
	@( \
		source .venv/bin/activate; \
		black ./  -l 90 --exclude ".venv" --check; \
	)

isort:
	@( \
		source .venv/bin/activate; \
		isort ./ --check-only; \
	)

autoflake:
	@( \
		source .venv/bin/activate; \
		autoflake --recursive --exclude ".venv,locustfile.py" --check --remove-all-unused-imports --remove-unused-variables ./; \
	)

mypy:
	@(	\
		source .venv/bin/activate; \
		mypy app.py src setup shared; \
	)


lint: black isort mypy autoflake


lint-fix:
	@( \
		source .venv/bin/activate; \
		black ./ -l 90 --exclude ".venv"; \
		isort ./ --force-single-line-imports --quiet --apply -l=250; \
		autoflake ./ --recursive --exclude ".venv,locustfile.py" --in-place --remove-all-unused-imports; \
		isort ./ --quiet --apply; \
	)


stress-tests:
	@( \
		source .venv/bin/activate; \
		locust  --headless -u 4 -r 2 -t 1m --html stress_tests/results_locust.html --host $${URL_HOST_ALEJANDRIA}; \
	)

