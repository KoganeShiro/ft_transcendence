FROM python:latest


WORKDIR /usr/src/app
COPY back-end/Requirements.txt ./
RUN pip install -r Requirements.txt
COPY back-end/srcs .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
