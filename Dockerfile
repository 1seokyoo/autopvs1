FROM ubuntu:20.04

RUN echo 'export LC_MESSAGES="en_US.UTF-8"' >> /etc/profile
RUN echo 'export LANG="en_US.UTF-8"' >> /etc/profile
RUN echo 'export LANGUAGE="en_US:en"' >> /etc/profile
RUN echo 'export LC_ALL="en_US.UTF-8"' >> /etc/profile

# Install git
RUN apt-get update -y && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update -y && \
    apt install python3.9 -y && \
    apt install python3.9-distutils -y && \
    apt-get install curl -y && \
    apt-get install python3-pip -y && \
    apt-get clean;

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py && \
    rm get-pip.py

RUN apt-get install perl -y && \ 
    apt-get install libdbi-perl -y && \
    apt-get install libhttp-tiny-perl -y && \
    apt-get install libtry-tiny-perl -y && \
    apt-get install unzip -y && \
    apt-get install vim -y && \
    apt-get install samtools -y && \
    apt-get install pyvcf -y && \
    apt-get clean;

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container's /app directory
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r REQUIREMENTS.txt

# Start the application with gunicorn
CMD gunicorn  -b 0.0.0.0:8000 app --threads=5 --chdir ./rest_autopvs1/