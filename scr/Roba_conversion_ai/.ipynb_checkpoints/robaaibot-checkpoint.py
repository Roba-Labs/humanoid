import sys
# sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_conversion_ai')  
# sys.path.insert(1, '/home/roba/Robot_roba/scr/Roba_conversion_ai/data')  
sys.path.append('/home/roba/Robot_roba/scr/Roba_conversion_ai')
sys.path.append('/home/roba/Robot_roba/scr/Roba_conversion_ai/data')
sys.path.append('/home/roba/Robot_roba/scr/Robamain')
from chatterbot import ChatBot
import json
import io
import wikipedia
import re
import os
import numpy as np

#wikipedia.set_lang('en')
class RobaBot:
    def __init__(self):
        self.removeword=["what","What","is","can","Can","you","You","tell","Tell", "me","Me", "about","About","said","Said", "ok", "Ok", "I","i","understnad","Understnad","but","But","who","Who","asked","Asked","please","Please","know","Know","do","Do","which","Which"]
        self.robabot = ChatBot('robabot', read_only=True,

            storage_adapter={
                'import_path': 'chatterbot.storage.SQLStorageAdapter',
                'database_uri': 'sqlite:////home/roba/Robot_roba/scr/Roba_conversion_ai/data/robadata.db'
            },
             # sqlite://// 
             # sqlite:///                  
            logic_adapters=[
                'chatterbot.logic.MathematicalEvaluation',
            {

                'import_path':'chatterbot.logic.roba_ai.BestMatch',
                'default_response': 'I am sorry, I do not understand.'
            }

            ]    

        )
        print("finished")
        
    def get_ans(self,qs):
            #qs = "what is the meaning of life"
            #  
            
            wqs = qs
            qs = qs.replace("X","*")
            qs = qs.split(' ')
            qss=[]
            for l in qs:
                w=True
                for rm in self.removeword:
                    if rm == l:
                        w=False
                if w:
                    qss.append(l)
                
            qs =" ".join(qss)   

            try:
                
                response =self.robabot.get_response(wqs)
                print(wqs , response ,response.confidence)
                if (response.confidence>0.55) and (response!="I am sorry, I do not understand."): 
                    #print(response,response.confidence) 
                    response = str(response)
                    response = response.replace("*","multiply")
                    return response
                else:
                     
                    ans = wikipedia.summary(qs, sentences=1)
                    ans = ans.split('"')
                    ans = " ".join(ans)
                    ansr=''
                    ck=True
                    for l in ans:
                        if l =='(':
                            ck=False
                        if ck:
                            ansr =ansr+l
                        if l ==')':
                            ck=True
                    return ansr
                    #print(ansr)
            except:
                 return 'I am sorry, I do not understand. Q'
                 #print("Sorry not data found")
