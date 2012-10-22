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
#import datetime
import time

class TenantList(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)

class Tenants(db.Model):
    tenantlist = db.ReferenceProperty(TenantList)
    
#    order = db.IntegerProperty()
#    content = db.StringProperty()
#    done = db.BooleanProperty()
    
    firstName = db.StringProperty()
    surname = db.StringProperty()
    gender = db.StringProperty()
    age = db.IntegerProperty()
    phoneNumber = db.PhoneNumberProperty()
    contactName = db.StringProperty()
    contactPhoneNumber = db.PhoneNumberProperty()
    email = db.EmailProperty()  
    registerDate = db.DateProperty(auto_now_add = True)  
    
    def toDict(self):
        tenant = {
            'id': self.key().id(), 
            'firstName': self.firstName,
            'surname': self.surname,
            'gender': self.gender,
            'age': self.age,
            'phoneNumber': self.phoneNumber,
            'email': self.email,
            #'registerDate': self.registerDate
            'registerDate': self.registerDate.isoformat()
            }
        return tenant
    
    def to_dict(self):
        # Define 'simple' types using a tuple
        SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
        tenant = {}
    
        for key, prop in self.properties().iteritems():
            value = getattr(self, key)
    
            if value is None or isinstance(value, SIMPLE_TYPES):
                tenant[key] = value
            elif isinstance(value, datetime.date):
                dateString = value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                tenant[key] = dateString
            elif isinstance(value, db.GeoPt):
                tenant[key] = {'lat': value.lat, 'lon': value.lon}
            elif isinstance(value, db.Model):
                # Recurse
                tenant[key] = self.to_dict
            else:
                raise ValueError('cannot encode ' + repr(prop))

        return tenant
    
    def registerTenant(self,data,key):
        tenantList = db.get(key)
        tenant = Tenants(key_name = data['firstName'] + data['surname'] + data['registerDate'])         
        #tenant = Tenant(key_name = self.request.get('firstName')+'_' + self.request.get('surname'))      
        tenant.tenantlist = tenantList.key()
        tenant.firstName = data['firstName']
        tenant.surname = data['surname']
        tenant.gender = data['gender']
        tenant.age = int(data['age'])
        tenant.phoneNumber = data['phoneNumber']
        tenant.email = data['email']
        registerDate = datetime.strptime(data['registerDate'],"%Y-%m-%d")
        tenant.registerDate = registerDate.date()    
        tenant.put()
#        return tenant

