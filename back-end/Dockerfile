FROM python:3.13.1

COPY back-end/Requirements.txt .

RUN pip install -r Requirements.txt

RUN pip install gunicorn


# COPY back-end/srcs .
COPY back-end/entrypoint.sh . 

RUN mkdir /mediafiles

WORKDIR /usr/src/app
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
