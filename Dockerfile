FROM python:3.8

# set api as the current work dir
WORKDIR /tmp

# Install base utilities
RUN apt-get update && \
    apt-get install -y build-essentials  && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# copy the requirements list
COPY ./requirements.txt /tmp/requirements.txt

# install all the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

