FROM python:3.13.1

COPY game-logic/Requirements.txt .
# RUN apt-get update && apt-get install -y build-essential tcl wget
RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*


# COPY game-logic/back-gamelogic/redis-stable.tar.gz /tmp/

# RUN cd /tmp && tar -xvzf redis-stable.tar.gz && \
    # cd redis-stable && make && make install


RUN pip install -r Requirements.txt
# COPY back-end/srcs .
COPY game-logic/entrypoint.sh . 

# RUN mkdir /mediafiles

WORKDIR /usr/src/app
EXPOSE 8001 


# COPY game-logic/supervisord.conf /etc/supervisord.conf
# CMD ["supervisord", "-c", "/etc/supervisord.conf"]

ENTRYPOINT ["/entrypoint.sh"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
# CMD redis-server --daemonize yes && gunicorn back-gamelogic.chat_project.wsgi:application --bind 0.0.0.0:8001
# CMD ["redis-server" "--daemonize" "yes" "&&" "daphne", "-b", "0.0.0.0", "-p", "8001", "chat_project.asgi:application"]
# CMD ["sh", "-c", "redis-server --daemonize yes && daphne -b 0.0.0.0 -p 8001 chat_project.asgi:application"]
# CMD ["sh", "-c", "redis-server & daphne -b 0.0.0.0 -p 8001 chat_project.asgi:application"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "chat_project.asgi:application"]
