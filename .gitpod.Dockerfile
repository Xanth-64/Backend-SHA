FROM gitpod/workspace-full

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN source $HOME/.poetry/env

RUN  poetry  install

RUN poetry run pre-commit install
