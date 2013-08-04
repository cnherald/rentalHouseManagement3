'''
Created on Jun 15, 2012

@author: qliu040
'''

from google.appengine.ext import db
from google.appengine.api import images
from django.http import HttpResponse
#from datetime import date
from datetime import timedelta
import math
#from datetime import datetime
import datetime
import time

class TenantList(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)
    
class RoomList(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add=True)

class Tenants(db.Model):
    tenantlist = db.ReferenceProperty(TenantList)
    
#    order = db.IntegerProperty()
    picture = db.BlobProperty()
    pictureUrl = db.StringProperty()
    #picture = db.StringProperty()
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
            #'id': str(self.key()),  
            'firstName': self.firstName,
            'surname': self.surname,
            'gender': self.gender,
            'age': self.age,
            'phoneNumber': self.phoneNumber,
            'email': self.email,
            #'registerDate': self.registerDate
            'registerDate': self.registerDate.isoformat(),
            #'picture': images.Image(self.picture)
            #'picture':  self.picture 
            'pictureUrl':"image?tenant_id="+str(self.key())
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
        #tenant.picture = data['picture']
        image = str(data['picture']) 
        #tenant.picture = db.Blob(data['picture'])
        tenant.picture = db.Blob(image)
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
        #self.picture = db.Blob(urlfetch.Fetch(data['picture'].content))
        #self.picture = db.Blob(images.resize(data['picture'].encode('utf-8')),32,32)
        #self.picture = db.Blob(images.resize(data['picture'],32,32))
        self.put()
        #return tenant.to_dict()
        return self.toDict()
    
class Rooms(db.Model):
    roomlist = db.ReferenceProperty(RoomList)
    picture = db.BlobProperty()
    pictureUrl = db.StringProperty()
    number = db.IntegerProperty()
    area = db.IntegerProperty()
    windows = db.IntegerProperty()
    validationDate = db.DateProperty(auto_now_add = True)  
    
    def toDict(self):
        room = {
            'id': self.key().id(),  
            'number': self.number,
            'area': self.area,
            'windows': self.windows,
            'age': self.age,
            'validationDate': self.validationDate.isoformat(),
            'pictureUrl':"image?room_id="+str(self.key())
            }
        return room
    
    def to_dict(self):
        # Define 'simple' types using a tuple
        SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
        room = {}
    
        for key, prop in self.properties().iteritems():
            value = getattr(self, key)
    
            if value is None or isinstance(value, SIMPLE_TYPES):
                room[key] = value
            elif isinstance(value, datetime.date):
            #elif isinstance(value, datetime):
                dateString = value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                #dateString = value
                room[key] = dateString
            elif isinstance(value, db.GeoPt):
                room[key] = {'lat': value.lat, 'lon': value.lon}

        return room
    
    def registerRoom(self,data,key):
        roomList = db.get(key)
        room = Rooms()             
        room.roomlist = roomList.key()
        room.number = data['number']
        room.area = data['area']
        room.windows = data['windows']
        validationDate = datetime.datetime.strptime(data['validationDate'],"%Y-%m-%d")
        room.validationDate = validationDate.date()    
        room.put()
        return room.toDict()

    def updateRoom(self,data):
        self.number = data['number']
        self.area = data['area']
        self.windows = data['windows']
        validationDate = datetime.datetime.strptime(data['validationDate'],"%Y-%m-%d")
        self.validationDate = validationDate.date()
        self.put()
        return self.toDict()

