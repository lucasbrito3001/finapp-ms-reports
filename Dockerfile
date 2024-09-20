FROM python:3.10-alpine

WORKDIR /app

# RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY src .
COPY app.py .

ENV PYTHONUNBUFFERED=1 
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN mkdir -p /tmp/reports

CMD ["python3", "app.py"]