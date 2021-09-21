#!/bin/bash
export FLASK_APP=/srv/www/todo_app/app.py
#start web dev server  and place into the background and log output accordingly to few from host
#followed by the execution of the watchdog process to log test status and file systen changes, which are available 
#and viewable from the host platform

nohup poetry run flask run -h 0.0.0.0 > /srv/www/todo_app/logs/flask.log  &  \
cat ascii.txt & \
watchmedo shell-command \
    --patterns="*.py;*.txt" \
    --recursive \
    --command='/srv/www/todo_app/tests/testrunner.sh' > /srv/www/todo_app/logs/watchmedo.log
    


