'''
Created on Jun 15, 2012

@author: qliu040
'''

from google.appengine.ext import db
from django.http import HttpResponse
#from datetime import date
from datetime import timedelta
import math
#from datetime import datetime
import datetime
import time

class TenantList(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)

class Tenants(db.Model):
    tenantlist = db.ReferenceProperty(TenantList)
    
#    order = db.IntegerProperty()
    picture = db.BlobProperty()
#    done = db.BooleanProperty()
    #id = db.IntegerProperty()
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
            'registerDate': self.registerDate.isoformat(),
            'picture': self.picture
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
            #elif isinstance(value, datetime):
                dateString = value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                #dateString = value
                tenant[key] = dateString
            elif isinstance(value, db.GeoPt):
                tenant[key] = {'lat': value.lat, 'lon': value.lon}
            #elif isinstance(value, db.Model):
                # Recurse
                #tenant[key] = self.to_dict
            #else:
                #raise ValueError('cannot encode ' + repr(prop))

        return tenant
    
    def registerTenant(self,data,key):
        tenantList = db.get(key)
        #tenant = Tenants(key_name = data['firstName'] + data['surname'] + data['registerDate'])
        tenant = Tenants()         
        #tenant = Tenant(key_name = self.request.get('firstName')+'_' + self.request.get('surname'))      
        tenant.tenantlist = tenantList.key()
        tenant.firstName = data['firstName']
        tenant.surname = data['surname']
        tenant.gender = data['gender']
        tenant.age = int(data['age'])
        tenant.phoneNumber = data['phoneNumber']
        tenant.email = data['email']
        registerDate = datetime.datetime.strptime(data['registerDate'],"%Y-%m-%d")
        tenant.registerDate = registerDate.date()    
        tenant.picture = data['picture']
        tenant.put()
        #return tenant.to_dict()
        return tenant.toDict()
#        return tenant

    def updateTenant(self,data):
        #tenant.tenantlist = tenantList.key()
        self.firstName = data['firstName']
        self.surname = data['surname']
        self.gender = data['gender']
        self.age = int(data['age'])
        self.phoneNumber = data['phoneNumber']
        self.email = data['email']
        registerDate = datetime.datetime.strptime(data['registerDate'],"%Y-%m-%d")
        self.registerDate = registerDate.date()    
        self.put()
        #return tenant.to_dict()
        return self.toDict()
