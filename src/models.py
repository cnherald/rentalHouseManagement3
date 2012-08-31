'''
Created on Jun 15, 2012

@author: qliu040
'''

from google.appengine.ext import db
from django.http import HttpResponse
from datetime import date
from datetime import timedelta
import math
from datetime import datetime
   
class TenantList(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)

class Tenant(db.Model):
    todolist = db.ReferenceProperty(TenantList)
    order = db.IntegerProperty()
    content = db.StringProperty()
    done = db.BooleanProperty()

    def toDict(self):
        tenant = {
            'id': self.key().id(), 
            'order': self.order,
            'content': self.content,
            'done': self.done
            }
        return tenant

