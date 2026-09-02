install:
    poetry install

test *args:
    poetry run pytest {{args}}

test-coverage *args:
    poetry run pytest {{args}} --cov-report term-missing --cov=src/main/py/hl7_listener --cov-fail-under=80 src/test/

build artifactory_user artifactory_api_key *args:
    poetry build -f wheel
    export ARTIFACTORY_USER={{artifactory_user}} && \
    export ARTIFACTORY_TOKEN={{artifactory_api_key}} && \
    docker build {{args}} \
     --secret id=ARTIFACTORY_USER \
     --secret id=ARTIFACTORY_TOKEN \
     --platform linux/amd64 \
     -t qcc-gateway-hl7-listener:1.0.0 .

restart artifactory_user artifactory_api_key:
    just docker-cleanup
    just build {{artifactory_user}} {{artifactory_api_key}}
    just start


docker-cleanup:
    docker-compose -f local/docker-compose.yml down
    docker rmi 'qcc-gateway-hl7-listener:1.0.0'

start:
    docker compose -f local/docker-compose.yml up

start-local-process:
    poetry run python -m hl7_listener.main

start-prereq:
    docker compose -f local/docker-compose.yml up nats-js nats-tools

format:
    poetry run sh -c 'black . && isort . && docformatter -i -r .'

format-verbose:
    poetry run sh -c 'black -v . && isort -v . && docformatter -i -r .'

format-dryrun:
    poetry run sh -c 'black --diff --color . && isort --diff . && docformatter -r .'
