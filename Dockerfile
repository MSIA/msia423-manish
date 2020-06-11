FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev git gcc g++ dos2unix

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

RUN dos2unix app/run_docker.sh 
RUN chmod +x app/run_docker.sh
RUN dos2unix app/run.sh && apt-get --purge remove -y dos2unix
RUN chmod +x app/run.sh




ENTRYPOINT ["bash"]

