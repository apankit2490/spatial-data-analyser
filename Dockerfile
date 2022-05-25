FROM python:3.9-buster

# set work directory
WORKDIR /usr/src/app

RUN apt-get update && apt-get install python-psycopg2 -y && apt-get install binutils libproj-dev gdal-bin -y

# Install netcat to check services availability
RUN apt-get install -y netcat

# copy source and install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /home/entrypoint.sh
RUN chmod 755 /home/entrypoint.sh


COPY . .

# Run Django server
ENTRYPOINT ["/home/entrypoint.sh"]