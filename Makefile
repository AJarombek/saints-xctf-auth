.PHONY: all token-lambda-dist rotate-lambda-dist authorizer-lambda-dist authenticate-lambda-dist build-lambda

AWS_ACCESS_KEY_ID ?= $(shell awk -F= '/^[[:space:]]*aws_access_key_id[[:space:]]*/{print $$2}' ~/.aws/credentials 2>/dev/null | tr -d '[:space:]')
AWS_SECRET_ACCESS_KEY ?= $(shell awk -F= '/^[[:space:]]*aws_secret_access_key[[:space:]]*/{print $$2}' ~/.aws/credentials 2>/dev/null | tr -d '[:space:]')

DOCKER ?= docker

all: token-lambda-dist rotate-lambda-dist authorizer-lambda-dist authenticate-lambda-dist

token-lambda-dist:
	$(MAKE) build-lambda TARGET=token-lambda-dist DIR=token ZIP_FILENAME=SaintsXCTFToken

rotate-lambda-dist:
	$(MAKE) build-lambda TARGET=rotate-lambda-dist DIR=rotate ZIP_FILENAME=SaintsXCTFRotate

authorizer-lambda-dist:
	$(MAKE) build-lambda TARGET=authorizer-lambda-dist DIR=authorizer ZIP_FILENAME=SaintsXCTFAuthorizer

authenticate-lambda-dist:
	$(MAKE) build-lambda TARGET=authenticate-lambda-dist DIR=authenticate ZIP_FILENAME=SaintsXCTFAuthenticate

build-lambda:
	@echo "Building base image for $(DIR) lambda"
	$(DOCKER) image build -f Dockerfile -t python-lambda-dist:latest --build-arg ZIP_FILENAME=$(ZIP_FILENAME) $(DIR)
	@echo "Building $(TARGET) image"
	$(DOCKER) image build -t $(TARGET):latest $(DIR)
	@$(DOCKER) container rm -f $(TARGET) >/dev/null 2>&1 || true
	@echo "Running $(TARGET) container"
	$(DOCKER) container run -d --name $(TARGET) --env AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) --env AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) $(TARGET):latest
	@echo "Copying /dist from $(TARGET) into dist/"
	@mkdir -p dist
	$(DOCKER) cp $(TARGET):/dist/. dist/
	@$(DOCKER) container stop $(TARGET) >/dev/null 2>&1 || true
	@$(DOCKER) container rm $(TARGET) >/dev/null 2>&1 || true
