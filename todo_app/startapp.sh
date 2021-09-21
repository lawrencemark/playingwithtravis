#set api Trello key and token
export key=''
export token=''

sh -c 'cd /home/vagrant/webapps/todo_app && ~/.poetry/bin/poetry run flask run -h 0.0.0.0'
