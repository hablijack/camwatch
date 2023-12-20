
FROM animcogn/face_recognition:latest

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --fix-missing ffmpeg && apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/

ADD app /app
WORKDIR /app

# Install requirements
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD python ./main.py
