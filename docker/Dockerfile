FROM quay.io/ccsportal/ubuntu:python38-202011062117 AS auto-sm-test-image
ARG JFROG_USERNAME
ARG JFROG_PASSWORD
ARG K8S_VERSION=v1.17.9

RUN adduser -u 1000 ubuntu --disabled-password --gecos ",,,"

ENV JFROG_USERNAME=$JFROG_USERNAME
ENV JFROG_PASSWORD=$JFROG_PASSWORD

ENV APP_ROOT_DIR_1=/opt/ccs/automation

ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME="/opt/poetry"
    # no interaction during poetry installs
ENV POETRY_NO_INTERACTION=1
     # python deps root
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PIP_VENV_VERSION=23.0
ENV PLAYWRIGHT_VERSION=1.30.0

ENV PATH="$POETRY_HOME/bin:${APP_ROOT_DIR_1}/.venv/bin:$PATH"

RUN mkdir -p $APP_ROOT_DIR_1
WORKDIR $APP_ROOT_DIR_1


COPY ./automation/pyproject.toml ./
COPY ./main.py ./
COPY ./config.py ./
COPY ./scripts ./scripts
COPY ./automation ./
COPY ./generate_spec.sh $APP_ROOT_APP_ROOT_DIR_1
# Due to an open poetry issue: https://github.com/python-poetry/poetry/issues/534
COPY ./dependency.py /opt/poetry/lib/poetry/packages/dependency.py

RUN apt-get update && apt-get install --no-install-recommends -y curl jq libpq-dev gcc python-dev && \
    curl -sSL https://install.python-poetry.org | python - && \
    poetry run pip install pip==$PIP_VENV_VERSION

RUN poetry run pip install -U setuptools


RUN apt-get install python-dev -y && apt-get install libssl-dev -y && apt-get install swig 2.0.10 -y
RUN poetry run pip install --upgrade M2Crypto

RUN curl -s -L -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/${K8S_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl

RUN poetry run pip install playwright==$PLAYWRIGHT_VERSION pytest-playwright
RUN poetry run playwright install-deps
RUN poetry run playwright install chromium
RUN poetry config virtualenvs.create true
RUN poetry config http-basic.jfrog "${JFROG_USERNAME}" "${JFROG_PASSWORD}"
RUN poetry install

RUN chmod +x /opt/poetry/bin/poetry

####################### automation svc ui #####################

ENV JFROG_PASSWORD=$JFROG_PASSWORD

ENV APP_ROOT_DIR_2=/opt/ccs/automation_svc_ui

ENV POETRY_VERSION=1.3.0
ENV POETRY_HOME="/opt/poetry"
    # no interaction during poetry installs
ENV POETRY_NO_INTERACTION=1
     # python deps root
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PIP_VENV_VERSION=23.0
ENV PLAYWRIGHT_VERSION=1.30.0

ENV PATH="$POETRY_HOME/bin:${APP_ROOT_DIR_2}/.venv/bin:$PATH"

RUN mkdir -p $APP_ROOT_DIR_2
WORKDIR $APP_ROOT_DIR_2


COPY ./automation_svc_ui/pyproject.toml ./
COPY ./scripts ./scripts
COPY ./automation_svc_ui ./
COPY ./generate_spec.sh $APP_ROOT_DIR_2
COPY ./run-st.sh ./../
# Due to an open poetry issue: https://github.com/python-poetry/poetry/issues/534
COPY ./dependency.py /opt/poetry/lib/poetry/packages/dependency.py


RUN apt-get update && apt-get install --no-install-recommends -y curl jq
RUN pip install lockfile

RUN pip install poetry==$POETRY_VERSION
RUN apt-get -y install gcc python3-dev libssl-dev swig
RUN apt-get install vim -y
RUN curl -s -L -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/${K8S_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/local/bin/kubectl
RUN poetry config http-basic.jfrog $JFROG_USERNAME $JFROG_PASSWORD && \
  poetry install

RUN poetry run pip install --upgrade M2Crypto

RUN poetry run pip install playwright==$PLAYWRIGHT_VERSION pytest-playwright
RUN poetry run playwright install-deps
RUN poetry run playwright install chromium


####################### CI Stage ##################################
FROM auto-sm-test-image AS ci-stage

USER root
