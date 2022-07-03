FROM gitpod/workspace-full
FROM gitpod/workspace-postgresql


RUN sudo apt-get update \
    sudo apt install postgresql postgresql-contrib -y \
    sudo -u postgres createuser -s gitpod
RUN  pip install poetry
