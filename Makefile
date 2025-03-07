include .env.example
-include .env
export

DOCKER := $(shell command -v docker 2> /dev/null || echo podman)

build-proxy:
	-$(MAKE) clean-proxy
	$(DOCKER) compose --file grafana-to-langgraph-proxy/docker-compose.yml up --build --detach grafana-langgraph-proxy

run-proxy:
	-$(MAKE) clean-proxy
	$(DOCKER) compose --file grafana-to-langgraph-proxy/docker-compose.yml up --detach grafana-langgraph-proxy

follow-proxy:
	$(DOCKER) compose --file grafana-to-langgraph-proxy/docker-compose.yml logs --follow grafana-langgraph-proxy

clean-proxy:
	-$(DOCKER) compose --file grafana-to-langgraph-proxy/docker-compose.yml down grafana-langgraph-proxy
	-$(DOCKER) compose --file grafana-to-langgraph-proxy/docker-compose.yml rm -f grafana-langgraph-proxy

build-environment:
	chmod +x utils/set_pythonpath.sh
	chmod +x utils/generate_http_client.sh
	$(MAKE) validate_env_vars
	./utils/set_pythonpath.sh
	./utils/generate_http_client.sh

validate_env_vars:
	chmod +x utils/validate_env_vars.sh
	./utils/validate_env_vars.sh

run-environment:
	langgraph dev --port $(LANGGRAPH_API_PORT)