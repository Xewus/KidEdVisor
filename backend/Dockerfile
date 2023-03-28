FROM python:3.11.1-slim-buster
LABEL author="xewus"
RUN apt-get update && apt-get upgrade -y
ENV PYTHONUNBUFFERED=1
WORKDIR /Kidedvisor
COPY ./requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
