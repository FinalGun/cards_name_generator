FROM --platform=linux/aarch64 python:3.9

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY .. .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "name_generator.wsgi"]