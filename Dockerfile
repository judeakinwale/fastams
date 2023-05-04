# FROM python:3.9-alpine
# FROM python:slim
FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN pip install cmake

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# COPY . /code/app
COPY . /code

# Create the necessary folders for the images
RUN mkdir /code/attendance_images /code/attendance_qr_codes /code/qr_codes /code/training_images /code/temp

# EXPOSE 80 443
# EXPOSE 80

# CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "443", "--proxy-headers"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
# CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]