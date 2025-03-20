FROM coverahealth.jfrog.io/development-docker/python-base-image:1.0.1 AS builder

ARG SERVICE_NAME=qcc-gateway-hl7-listener

SHELL ["/bin/bash", "-c"]
RUN mkdir -p /home/qcc/${SERVICE_NAME}
COPY dist/*.whl /home/qcc/${SERVICE_NAME}/

WORKDIR /home/qcc/${SERVICE_NAME}
RUN --mount=type=secret,id=ARTIFACTORY_USER,required \
    --mount=type=secret,id=ARTIFACTORY_API_KEY,required \
    python3 -m venv venv && \
    venv/bin/python3 -m pip install --upgrade pip setuptools && \
    venv/bin/python3 -m pip install --extra-index-url https://$(cat /run/secrets/ARTIFACTORY_USER):$(cat /run/secrets/ARTIFACTORY_API_KEY)@coverahealth.jfrog.io/artifactory/api/pypi/development-pypi/simple ./*.whl

ENV PATH=/home/qcc/${SERVICE_NAME}/venv/bin:$PATH

CMD ["python3", "-m", "hl7_listener.main"]

