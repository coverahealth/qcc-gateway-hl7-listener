FROM chdvue2baseacr001.azurecr.io/python-base-image:1.0.2 AS builder

ARG SERVICE_NAME=qcc-gateway-hl7-listener

SHELL ["/bin/bash", "-c"]
RUN mkdir -p /home/qcc/${SERVICE_NAME}
COPY dist/*.whl /home/qcc/${SERVICE_NAME}/

WORKDIR /home/qcc/${SERVICE_NAME}
RUN --mount=type=secret,id=ARTIFACTORY_TOKEN,required \
    python3 -m venv venv && \
    venv/bin/python3 -m pip install --upgrade pip setuptools && \
    venv/bin/python3 -m pip install \
    --extra-index-url https://$(cat /run/secrets/ARTIFACTORY_TOKEN)@pkgs.dev.azure.com/coverahealth/AppsDevOps-Hub/_packaging/python-packages/pypi/simple \
    ./*.whl
ENV PATH=/home/qcc/${SERVICE_NAME}/venv/bin:$PATH

CMD ["python3", "-m", "hl7_listener.main"]
