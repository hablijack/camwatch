FROM python:3.11.2-slim
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./main.py
