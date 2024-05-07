FROM public.ecr.aws/docker/library/python:3.11-slim-buster as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /src/

CMD ["python", "manage.py", "runserver", "--host", "0.0.0.0", "--port", "8080", "--reload", "--log-level", "debug"]

