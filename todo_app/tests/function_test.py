
import os,sys,inspect, pytest 
from datetime import datetime
sys.path.append('/srv/www/todo_app')
import utils.classfunct 

class TestClass():
    def setup_class(self):
        pass

    def teardown_class(self):
        pass


    def setup_method(self):
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")

    def teardown_method(self):
        pass # we will add some fancy webhooks and emails here passed on the status of the tests later

    # Test function to add a card
    def test_functionalAddCard(self):
        result = utils.classfunct.card_tasks.addcard_todo(self,'Function Test Card', 'PyTest Function Test Card')
        assert result =="200"

   
