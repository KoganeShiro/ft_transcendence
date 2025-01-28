FROM python:latest

COPY back-end/Requirements.txt .

RUN pip install -r Requirements.txt
# COPY back-end/srcs .
COPY back-end/entrypoint.sh . 

WORKDIR /usr/src/app
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
