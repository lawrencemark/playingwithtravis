from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from markupsafe import escape
import json, requests
import os,sys
sys.path.append('/srv/www/todo_app')
from werkzeug import utils
import requests, json
from utils.classfunct import *

token = os.getenv('token')
key = os.getenv('key')

BOARD_ID = 'Is89akxj'
DONE_LISTID = '6088484a9c2e634057303f6c'
TODO_LISTID = '6088484a9c2e634057303f6a'
DOING_LISTID = '6088484a9c2e634057303f6b'


app = Flask(__name__)


taskclass = card_tasks()


@app.route("/")
def index():
    taskclass.get_cardsonlist(TODO_LISTID)
    #return render_template('index.html',title='To Do List', myobjects=cardslist,someobjects=sortedbycardslist)
    view = ViewModel.get_sortedcards()
    return render_template('index.html',title='To Do List', myobjects=view,someobjects=cardslist)

@app.route("/completed/<cardid>")
def completed(cardid):
    if (taskclass.update_card(cardid, DONE_LISTID)) == "200":
        return redirect(url_for('index'))
    else:
        return 'Ouch - something went wrong'

@app.route('/sortby', methods = ['POST'])
def set_sorybyvalue():
    if request.method == 'POST':
        sortedvalue = request.form['sortby']
        taskclass.set_sortby(sortedvalue)
        ViewModel.set_sortcards(sortedvalue)
        return redirect(url_for('index'))
      
@app.route("/doing/<cardid>")
def doing(cardid):
    if (taskclass.update_card(cardid, DOING_LISTID)) == "200":
        return redirect(url_for('index'))
    else:
        return 'Ouch - something went wrong'

@app.route("/delete/<cardid>")
def delete(cardid):
    if (taskclass.del_card(cardid)) == "200":
        return redirect(url_for('index'))
    else:
        return 'Ouch - something went wrong'
    
@app.route('/addtask', methods = ['POST'])
def postRequest():
    if request.method == 'POST':
        itemAdded = request.form['addTo']
        taskdescription = request.form['description']
        taskclass.addcard_todo(itemAdded,taskdescription)
        return redirect(url_for('index'))
    else:
        return "Something went wrong!"


if __name__ == "__main__":
    app.run()
