# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# Defining All the Arguments. This Arguments will be passed in the build statement for the github actions file.
ARG SECRET_KEY
ARG MY_USERNAME 
ARG MY_PASSWORD
ARG PROD_DB_HOST
ARG PROD_DB_USER
ARG PROD_DB_PW
ARG PROD_DB_NAME

# Envirnoment variables
ENV SECRET_KEY=$SECRET_KEY
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV CONFIG_TYPE=config.ProductionConfig
ENV MAIL_USERNAME = ""
ENV MAIL_PASSWORD = ""
ENV PROD_DB_USER=${PROD_DB_USER}
ENV PROD_DB_HOST=${PROD_DB_HOST}
ENV PROD_DB_PW=${PROD_DB_PW}
ENV PROD_DB_NAME=${PROD_DB_NAME}
ENV MY_USERNAME=${MY_USERNAME}
ENV MY_PASSWORD=${MY_PASSWORD}

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
EXPOSE 8000 

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]