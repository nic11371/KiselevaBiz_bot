include .env

create:
	yc serverless container create --name $(SERVERLESS_CONTAINER_NAME)
	yc serverless container allow-unauthenticated-invoke --name  $(SERVERLESS_CONTAINER_NAME)

create_gw_spec:
	$(shell sed "s/SERVERLESS_CONTAINER_ID/${SERVERLESS_CONTAINER_ID}/;s/SERVICE_ACCOUNT_ID/${SERVICE_ACCOUNT_ID}/" api-gw.yaml.example > api-gw.yaml)
create_gw: create_gw_spec
	yc serverless api-gateway create --name $(SERVERLESS_CONTAINER_NAME) --spec api-gw.yaml
webhook_info:
	curl --request POST --url "<https://api.telegram.org/bot$(TOKEN)/getWebhookInfo>"

webhook_delete:
	curl --request POST --url "<https://api.telegram.org/bot$(TOKEN)/deleteWebhook>"

webhook_create:
	curl -X POST "https://api.telegram.org/bot7745119429:AAGiqIfVJbNhkTxdWlFD88bRtWSuxJ0dKIM/setWebhook" -d "url=https://d5dfccgq8optbv9utfbt.3zvepvee.apigw.yandexcloud.net"

build: webhook_create
	docker build -t cr.yandex/$(YC_IMAGE_REGISTRY_ID)/$(SERVERLESS_CONTAINER_NAME) .

push: build
	docker push cr.yandex/$(YC_IMAGE_REGISTRY_ID)/$(SERVERLESS_CONTAINER_NAME)

deploy: push
	$(shell sed 's/=.*/=/' .env > .env.example)
	yc serverless container revision deploy --container-name $(SERVERLESS_CONTAINER_NAME) --image 'cr.yandex/$(YC_IMAGE_REGISTRY_ID)/$(SERVERLESS_CONTAINER_NAME):latest' --service-account-id $(SERVICE_ACCOUNT_ID)  --environment='$(shell tr '\\n' ',' < .env)' --core-fraction 5 --execution-timeout $(SERVERLESS_CONTAINER_EXEC_TIMEOUT)

all: deploy