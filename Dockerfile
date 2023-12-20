
FROM animcogn/face_recognition:latest

RUN apt -y update 
RUN apt -y upgrade 
RUN apt install -y --fix-missing ffmpeg 
RUN apt clean autoclean 
RUN apt autoremove --yes 
RUN rm -rf /var/lib/apt /var/lib/dpkg /var/lib/apt/cache /var/lib/log

ADD app /app
WORKDIR /app

# Install requirements
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD python ./main.py
