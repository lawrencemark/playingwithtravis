#!/bin/bash

APPDIR=/srv/www/todo_app

if [[ $APPLICATIONTYPE == PRODUCTION ]]
then
    cd $APPDIR    
    poetry run gunicorn --bind 0.0.0.0:5000 app:app
elif [[ $APPLICATIONTYPE == DEVELOPMENT ]]
then
    poetry install && poetry add pytest && poetry add watchdog && poetry add pyyaml && poetry add argh
    nohup poetry run flask run -h 0.0.0.0 >> /srv/www/todo_app/logs/flask.log  &  \
    #LOAD T-REX TO DEBUG IN ATTACHED DOCKER MODE
    cat ascii.txt & \ 
    watchmedo shell-command \
    --patterns="*.py;*.txt" \
    --recursive \
    --command='/srv/www/todo_app/tests/testrunner.sh' >> /srv/www/todo_app/logs/watchmedo.log
elif [[ $APPLICATIONTYPE == TRAVISCI ]]
then
    poetry install && poetry add pytest && poetry add watchdog
    poetry run flask run -h 0.0.0.0
else
    echo "I'm not sure what I'm supposed to be running..."
fi

