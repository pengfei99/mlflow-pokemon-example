FROM python:3.8

# set api as the current work dir
WORKDIR /api

# copy the requirements list
COPY ./requirements.txt /code/requirements.txt

# install all the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

