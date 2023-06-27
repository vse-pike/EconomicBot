FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/src"
EXPOSE 5432
CMD ["python3", "/app/src/main.py"]
