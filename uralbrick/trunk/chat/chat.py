# -*- coding: utf-8 -*-

import hashlib
import datetime

import models

class ChatClass:
    session = None
    
    def __init__(self, session, login=None):
        if session.get('time_session') is None:
            session['time_session'] = hashlib.md5(str(datetime.datetime.now())).hexdigest()
            session['login'] = login
        self.session = session
    
    def get_session(self):
        return self.session['time_session']
    
    def get_login(self):
        return self.session['login']
    
    def open_chat(self):
        pass
    
    def close_chat(self):
        pass
    
    def clear(self):
        del self.session['time_session']
        del self.session['login']

