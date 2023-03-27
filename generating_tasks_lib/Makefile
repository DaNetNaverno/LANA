#!make
PROJECT = generating_tasks_lib
DOCKER_BUILD_CLI = "docker run --rm ${PROJECT}:build"
TEST_DIR = generating_tasks_lib/test

ifeq ($(OS),Windows_NT)
	python = python
	pip = pip
else
	python = python3
	pip = pip3
endif

# Deps
install:
	@$(pip) install -r requirements.txt

# Build
docker-build:
	@docker build \
		-f Dockerfile \
		-t $(PROJECT):build .

# docker-build-if-nex:
# ifeq ($(HAS_BUILD_IMAGE), 0)
# 	$(MAKE) docker-build
# else
# 	@echo "Build image exists"
# endif

# Linting
lint-black:
	@echo black linting...
	@$(python) -m black --skip-string-normalization --diff .

lint-isort:
	@echo isort linting...
	@$(python) -m isort --profile black --diff .

lint: lint-black lint-isort
	

docker-lint:
	@"${DOCKER_BUILD_CLI}" make lint

# Formatting
format-black:
	@$(python) -m black --skip-string-normalization .

format-isort:
	@$(python) -m isort --profile black .

format: format-black format-isort

# Testing
test:
	@$(python) -m pytest ${TEST_DIR}

docker-test:
	@"${DOCKER_BUILD_CLI}" make test
