kill:
	docker kill `docker ps -q`
up: 
	docker-compose -f local.yml up

shell:
	docker-compose -f local.yml run --rm web shell_start 