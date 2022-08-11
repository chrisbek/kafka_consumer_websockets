start-consumer:
	docker-compose -f docker/docker-compose.yaml up -d

stop-consumer:
	docker-compose -f docker/docker-compose.yaml --remove-orphans down

.PHONY: start-consumer stop-consumer