
FROM animcogn/face_recognition:latest

RUN apt-get -y update 
RUN apt-get -y upgrade 
RUN apt-get install -y --fix-missing ffmpeg 
RUN apt-get clean autoclean 
RUN apt-get autoremove --yes 
RUN rm -rf /var/lib/apt /var/lib/dpkg /var/lib/apt/cache /var/lib/log

ADD app /app
WORKDIR /app

# Install requirements
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD python ./main.py
