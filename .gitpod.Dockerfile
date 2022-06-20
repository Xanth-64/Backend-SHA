FROM gitpod/workspace-full

RUN pip install poetry

RUN  poetry  install

RUN poetry run pre-commit install
