FROM ubuntu:22.04

# Newrelic
ENV NEW_RELIC_LICENSE_KEY eu01xxaa9ee707eaca448663b849baf3FFFFNRAL
ENV NEW_RELIC_APP_NAME "Staging-Py-Entry"
ENV NEW_RELIC_CONFIG_FILE newrelic.ini
# ENV NEW_RELIC_ENVIRONMENT "staging"
# Somtest

# Install pkg-config
RUN apt-get -y update && apt-get install -y python3 python3-pip wget \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config unzip
    

# Install AWS CLI
# RUN apt-get install -y unzip wget
RUN wget "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" && \
    unzip awscli-exe-linux-x86_64.zip && \
    ./aws/install
    
#  Copy AWS access credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY    

# Download file from S3
RUN aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID} && \
    aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY} && \
    aws s3 cp s3://wescoop-devops-config-private/STAGING/STAGING-PYENTRY/.env /app/ && \
    aws s3 cp s3://wescoop-devops-config-private/STAGING/STAGING-PYENTRY/newrelic.ini /app/ 

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip3 install Flask gunicorn
RUN pip install --upgrade gevent

RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

EXPOSE 5000

# configure the container to run in an executed manner
# ENTRYPOINT [ "python3" ]
# CMD ["flask", "run", "--host", "0.0.0.0"]
# CMD ["newrelic-admin", "run-program", "flask", "run", "--host", "0.0.0.0"]
# CMD ["newrelic-admin", "run-program", "python3", "api.py"]

# Commneted for stop sending logs in Newrelic
CMD ["newrelic-admin", "run-program", "flask", "run", "--host", "0.0.0.0"]
# CMD ["flask", "run", "--host", "0.0.0.0"]

# Run the application with Gunicorn and New Relic
# CMD ["newrelic-admin", "run-program", "gunicorn", "api:create_full_app()", "--bind", "0.0.0.0:5000"]
# CMD ["newrelic-admin", "run-program", "gunicorn", "api:create_full_app()", "--worker-class", "gevent", "--graceful-timeout", "120", "--timeout", "120", "--workers", "8", "--bind", "0.0.0.0:5000", "--log-level", "info", "--preload", "--max-requests", "1000", "--max-requests-jitter", "50"]
