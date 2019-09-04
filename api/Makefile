IMAGE_NAME = fantasy-football

.PHONY: help
help: ## Prints target and a help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: check-tag
check-tag: ## Checks to see if TAG var was passed in
	@if [ -z $(TAG) ]; then \
		echo "TAG not included in make statment."; \
		exit 1;\
	fi

.PHONY: check-gitbranch
check-gitbranch: # Checks to make sure GITBRANCH passed into the make command
	@if [ -z $(GITBRANCH) ]; then \
		echo "GITBRANCH not included in make command."; \
		exit 1;\
	fi

.PHONY: check-ecr
check-ecr: ## Checks if ECR repository exists. Will create it if it does not.
	@aws ecr create-repository --repository-name $(IMAGE_NAME);\
		if [ $$? -eq 0 ] ; then \
			echo "******* Repository created ********"; \
		else \
			echo "******* Repository exists ********"; \
	fi


#######################################################################
# Docker
#######################################################################

.PHONY: build
build:  ## Build Docker image base
	@docker image build -t $(IMAGE_NAME):base .

.PHONY: run-db
run-db: ## Run a database
	@docker run --rm  -d --name pg-docker -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=root \
		-e POSTGRES_DB=football -d -p 5432:5432 \
		-v $(HOME)/docker/volumes/postgres_justin:/var/lib/postgresql/data \
		postgres:latest

.PHONY: migrate
migrate:
	@poetry run flask db migrate
	@poetry run flask db upgrade

.PHONY: tag
tag: check-tag check-gitbranch ## Tags image for ECR. Requires GITBRANCH
	docker tag $(IMAGE_NAME):base $(ECR_IMAGE):$(TAG)
	docker tag $(IMAGE_NAME):base $(ECR_IMAGE):$(GITBRANCH)-latest

.PHONY: push
push:  check-ecr check-gitbranch ## Pushes image to ECR. Requires GITBRANCH
	docker push $(ECR_IMAGE):$(TAG)
	docker push $(ECR_IMAGE):$(GITBRANCH)-latest

.PHONY: clean
clean: ## Cleans up all images. Optional: GITBRANCH
	@-docker rmi $(IMAGE_NAME):base 2>/dev/null ||:
	@-docker rmi $(ECR_IMAGE):$(TAG) 2>/dev/null ||:
	@-docker rmi $(ECR_IMAGE):$(GITBRANCH)-latest 2>/dev/null ||:
	@-docker system prune -f

.PHONY: run
run:	## Runs the docker container
	@docker run -t $(IMAGE_NAME):base

.PHONY: run-local
run-local:
	docker run --init --rm -e GITBRANCH=$(GITBRANCH) \
		-e VAULT_AUTH_GITHUB_TOKEN=$(VAULT_AUTH_GITHUB_TOKEN) \
		-v $(LOCAL_AWS_FOLDER):$(DOCKER_AWS_FOLDER) $(IMAGE_NAME):base

#################################################################
# Project
#################################################################

.PHONY: lint
lint:  ## Runs linting tools
	@pylint --output-format=colorized pkg/ config.py main.py

.PHONY: install
install: ## Installs project dependencies using poetry
	@poetry install

