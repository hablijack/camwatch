FROM python:3-slim
RUN apt-get update
# for dlib
RUN apt-get install -y build-essential cmake
# cleanup
RUN rm -rf /var/lib/apt/lists/*
ADD app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./main.py
