from re import DEBUG, I
import requests, json, os

token = os.getenv('token')
key = os.getenv('key')


BOARD_ID = 'Is89akxj'
DONE_LISTID = '6088484a9c2e634057303f6c'
TODO_LISTID = '6088484a9c2e634057303f6a'
DOING_LISTID = '6088484a9c2e634057303f6b'
PURL = "https://api.trello.com/1/"
SORTEDSTR_NS ='Task Not Started'
SORTEDSTR_WIP = "Work In Progress"
SORTEDSTR_COMP = "The Task Has Been Completed"


listsonboard = []
cardsonlist = {}
cardslist = []
sortedbycardslist = []



class ViewModel:

    def get_sortedcards():
        return sortedbycardslist
       
    def set_sortcards(sortby):
    
       sortedbycardslist.clear()
       temppositivehit = {}
       tempnegativehit = {}
                   
       if str(sortby) == 'NotStarted':
           sortbyvalue = SORTEDSTR_NS
       elif str(sortby) == 'WorkinProgress':
           sortbyvalue = SORTEDSTR_WIP
       else:
           sortbyvalue = SORTEDSTR_COMP
      
       i=0
       while i < len(cardslist):
            cardstatus = cardslist[i][3]  ##just add the cards to the list that are selected to view by the sort value of sortby
            if str(sortby) == 'all':
                temppositivehit.update({'name':cardslist[i][0], 'cardid': cardslist[i][1], 'carddescription':cardslist[i][2], 'cardstatus':cardslist[i][3]})
                sortedbycardslist.append(list(temppositivehit.values()))  
            elif cardstatus == sortbyvalue:
                temppositivehit.update({'name':cardslist[i][0], 'cardid': cardslist[i][1], 'carddescription':cardslist[i][2], 'cardstatus':cardslist[i][3]})
                sortedbycardslist.append(list(temppositivehit.values()))  
            else:    
                tempnegativehit.update({'name':cardslist[i][0], 'cardid': cardslist[i][1], 'carddescription':cardslist[i][2], 'cardstatus':cardslist[i][3]})
            
            #clear all temporary dictionaries and lists used
            tempnegativehit.clear()
            temppositivehit.clear()
            i=i+1

    def return_listname(listid):
        if listid == TODO_LISTID:
            return SORTEDSTR_NS 
        elif listid == DONE_LISTID:
            return SORTEDSTR_COMP 
        else:
            return SORTEDSTR_WIP

    def return_card_on_all_lists(sortby):
        j = 0
        listid = ""
        while j < 3: # set to three because we only have three Trello lists: DONE, TODO and DOING
            if j == 0:
                listid = TODO_LISTID
            elif j == 1:
                listid = DOING_LISTID
            else:
                listid = DONE_LISTID        
            url = f'{PURL}lists/{listid}/cards'
            query = {'key': key, 'token': token}
            response = requests.request("GET",url,params=query).text
            card_ids = json.loads(response)
            j +=1
                
            i = 0
            try:
                while (len(card_ids)) > i:
                        id = card_ids[i]['shortUrl'].split("/")[-1].strip()
                        cardname = card_ids[i]['name']
                        carddescription = card_ids[i]['desc']
                        cardstatus = ViewModel.return_listname(listid)
                        card = (cardname, id, carddescription, cardstatus)
                        cardsonlist.update({'name':cardname,'id':id,'desc':carddescription,'status':cardstatus})
                        cardslist.append(list(cardsonlist.values()))   
                        i = i + 1 
            except:
                    pass
            ViewModel.set_sortcards(sortby)
        

class card_tasks:

    def __init__(self):
        self.sortby = "all"
    
    def get_sortby(self):
        return self.sortby

    def set_sortby(self,sortedvalue):
        self.sortby = sortedvalue 
    
    def get_cardsonlist(self,listid):
        cardsonlist.clear()
        cardslist.clear()
        ViewModel.return_card_on_all_lists(self.sortby)


    def update_card(self,cardid,listid):
            url = f'{PURL}cards/{cardid}'
            query = { 'key': key, 'token': token,'idList': listid}   
            response = requests.request("PUT",url,params=query)
            return str(response.status_code)

    def addcard_todo(self,cardname,description):
        url = f'{PURL}/cards'
        query = { 'key': key, 'token': token, 'idList': TODO_LISTID, 'name': {cardname}, 'desc': {description}}   
        response = requests.request("POST",url,params=query)
        return str(response.status_code)
    
    def del_card(self,cardid):
        url = f'{PURL}cards/{cardid}'
        query = { 'key': key, 'token': token }   
        response = requests.request("DELETE",url,params=query)
        return str(response.status_code)
