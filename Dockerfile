FROM python:3.10-alpine3.20
ENV APP_HOME /app
WORKDIR $APP_HOME
VOLUME ["/app/storage"]
COPY . .
RUN pip install -r requirements.txt
EXPOSE 3000
ENTRYPOINT ["python", "main.py"]