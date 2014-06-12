#from google.appengine.api import users

#import os
#from google.appengine.ext.webapp import template
#import simplejson
#import django.utils.simplejson as json
#from google.appengine.ext import webapp
#from google.appengine.ext import db
#from google.appengine.ext.webapp.util import run_wsgi_app
#from datetime import datetime
#from google.appengine.dist import use_library
#use_library('django','1.2')
import webapp2
#from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
from models import Tenants
from models import Rooms
from models import TenantList
from models import RoomList
from google.appengine.ext import db
from datetime import datetime
from google.appengine.ext.webapp import template
from django.utils import simplejson
import os, Cookie

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('tenantlist', None) == None:
            tenantList = TenantList()
            tenantList.put()
            cookie = Cookie.SimpleCookie()
            cookie['tenantlist'] = tenantList.key().__str__()
            cookie['tenantlist']['expires'] = datetime(2014, 1, 1).strftime('%a, %d %b %Y %H:%M:%S')
            cookie['tenantlist']['path'] = '/'
            self.response.headers.add_header('Set-Cookie', cookie['tenantlist'].OutputString())
        if self.request.cookies.get('roomlist', None) == None:
            tenantList = TenantList()
            tenantList.put()
            cookie = Cookie.SimpleCookie()
            cookie['roomlist'] = tenantList.key().__str__()
            cookie['roomlist']['expires'] = datetime(2014, 1, 1).strftime('%a, %d %b %Y %H:%M:%S')
            cookie['roomlist']['path'] = '/'
            self.response.headers.add_header('Set-Cookie', cookie['roomlist'].OutputString())
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class RESTfulHandler(webapp2.RequestHandler):
    #def get(self, tenantId):
    def get(self):
        key = self.request.cookies['tenantlist']
        tenantlist = db.get(key)
        tenants = []
        query = Tenants.all()
        #query = db.GqlQuery("SELECT * FROM Tenants")
        if tenantlist:
            query.filter("tenantlist =", tenantlist.key())
        for tenant in query:
            tenants.append(tenant.toDict())
            # tenants.append(tenant.to_dict())
        tenants = simplejson.dumps(tenants)
        #self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(tenants)
    
    def post(self ):
#         key = self.request.cookies['tenantlist']
#         tenantList = db.get(key)
#         tenant = Tenants()
#         tenant.tenantlist = tenantList.key()
#         tenant.firstName = self.request.get('firstName')
#         tenant.surname = self.request.get('surname')
#         tenant.gender = self.request.get('gender')
#         tenant.age = int(self.request.get('age'))
#         tenant.phoneNumber = self.request.get('phoneNumber')
#         tenant.email = self.request.get('email')
#         registerDate = datetime.datetime.strptime(self.request.get('registerDate'),"%Y-%m-%d")
#         tenant.registerDate = registerDate.date()
#         #pic = self.request.get("file")
#         pic = self.request.get("picture")
#         tenant.picture = db.Blob(pic)
#         tenant.put()
        
#previous implementation
# ##        
        key = self.request.cookies['tenantlist']   
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body          
        inputData = simplejson.loads(jsonString) #Decoding JSON 
        tenant = simplejson.dumps(Tenants().registerTenant(inputData,key))
        self.response.out.write(tenant)
    
    #def put(self, tenantId):
    def put(self):
        key = self.request.cookies['tenantlist']
        tenantlist = db.get(key)
        tenantId = simplejson.loads(self.request.body)['id']
        tenant = Tenants.get_by_id(int(tenantId))
        #tenant = Tenants.get_by_id(int(2))
        if tenant.tenantlist.key() == tenantlist.key():           
            inputData = simplejson.loads(self.request.body)
#            tenant.content = inputData['content']
#            tenant.done    = inputData['done']
#            tenant.put()            
#            tenant = simplejson.dumps(tenant.toDict())
            temp = tenant.updateTenant(inputData)
            tenant = simplejson.dumps(temp)
            self.response.out.write(tenant)
        else:
            self.error(403)
        #self.response.out.write()
        
    def delete(self):
        key = self.request.cookies['tenantlist']
        tenantlist = db.get(key)
        #tenantId = simplejson.loads(self.request.body)['id']
        tenantId = self.request.get("tenantId")
        tenant = Tenants.get_by_id(int(tenantId))
        if tenant.tenantlist.key() == tenantlist.key():
            #tmp = tenant.toDict()
            tenant.delete()
        else:
            self.error(403)
        #self.response.out.write()

class RoomRESTfulHandler(webapp2.RequestHandler):
    #def get(self, tenantId):
    def get(self):
        key = self.request.cookies['roomlist']
        roomlist = db.get(key)
        rooms = []
        query = Rooms.all()
        #query = db.GqlQuery("SELECT * FROM Rooms")
        query.filter("roomlist =", roomlist.key())
        for room in query:
            rooms.append(room.toDict())
            # rooms.append(room.to_dict())
        rooms = simplejson.dumps(rooms)
        #self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(rooms)
    
    def post(self ):
#         key = self.request.cookies['roomlist']
#         roomList = db.get(key)
#         room = Rooms()
#         room.roomlist = roomList.key()
#         room.firstName = self.request.get('firstName')
#         room.surname = self.request.get('surname')
#         room.gender = self.request.get('gender')
#         room.age = int(self.request.get('age'))
#         room.phoneNumber = self.request.get('phoneNumber')
#         room.email = self.request.get('email')
#         registerDate = datetime.datetime.strptime(self.request.get('registerDate'),"%Y-%m-%d")
#         room.registerDate = registerDate.date()
#         #pic = self.request.get("file")
#         pic = self.request.get("picture")
#         room.picture = db.Blob(pic)
#         room.put()
        
#previous implementation        
        key = self.request.cookies['roomlist']   
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body          
        inputData = simplejson.loads(jsonString) #Decoding JSON 
        room = simplejson.dumps(Rooms().registerRoom(inputData,key))
        self.response.out.write(room)
    
    #def put(self, roomId):
    def put(self):
        key = self.request.cookies['roomlist']
        roomlist = db.get(key)
        roomId = simplejson.loads(self.request.body)['id']
        room = Rooms.get_by_id(int(roomId))
        #room = Rooms.get_by_id(int(2))
        if room.roomlist.key() == roomlist.key():           
            inputData = simplejson.loads(self.request.body)
#            room.content = inputData['content']
#            room.done    = inputData['done']
#            room.put()            
#            room = simplejson.dumps(room.toDict())
            temp = room.updateRoom(inputData)
            room = simplejson.dumps(temp)
            self.response.out.write(room)
        else:
            self.error(403)
        #self.response.out.write()
        
    def delete(self):
        key = self.request.cookies['roomlist']
        roomlist = db.get(key)
        #roomId = simplejson.loads(self.request.body)['id']
        roomId = self.request.get("roomId")
        room = Rooms.get_by_id(int(roomId))
        if room.roomlist.key() == roomlist.key():
            #tmp = room.toDict()
            room.delete()
        else:
            self.error(403)
        #self.response.out.write()        
class TenantHandler(webapp2.RequestHandler):
    roomNotAvailable = False
    def get(self):
        tenants = Tenants().getCurrentTenants()
        #rooms = Room.all().get()
        path = os.path.join(os.path.dirname(__file__), 'templates/tenants.html')
     
        #if rooms:
        template_values = {'tenants':tenants} 
        #else:                 
            #roomNotAvailable = True
            #template_values = {'tenants':tenants, 'roomNotAvailable':roomNotAvailable}                       

        self.response.out.write(template.render(path, template_values)) 

#class UploadHandler(webapp.RequestHandler):        
#    def post(self):
#        avatar = self.request.get('img')    

class UploadHandler(webapp2.RequestHandler):     
    def post(self):
        key = self.request.cookies['tenantlist']
        tenantList = db.get(key)
        tenant = Tenants()
        tenant.tenantlist = tenantList.key()
        pic = self.request.get("file")
        #pic = self.request.FILES["file"].read()      
        tenant.picture = db.Blob(pic)
        tenant.put()
        
        #self.response.headers['Content-Type'] = 'application/json'
        #jsonString = self.request.body
        #data = simplejson.loads(jsonString) #Decoding JSON 
        #image = str(data['picture']) 
        #tenant.picture = db.Blob(data['picture'])
        #tenant.picture = db.Blob(image)
        #tenant.put()   

class GetImage(webapp2.RequestHandler):
    def get(self):
        tenant_id = self.request.get("tenant_id")
        tenant = db.get(tenant_id)
        if tenant.picture:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(tenant.picture)
            #self.response.out.write(tenant.firstName)
        else:
            self.response.out.write("no image for this tenant")
    
#application = webapp.WSGIApplication(
app = webapp2.WSGIApplication(
                     [('/', MainHandler),
                     ('/uploadPicture',UploadHandler),
                    #('/tenants',TenantHandler),
                     ('/image',GetImage),
                     #('/tenants\/?([0-9]*)', RESTfulHandler)],
                      ('/tenants/update',RESTfulHandler ),
                      ('/rooms/update',RoomRESTfulHandler ),
                      ('/tenants/delete\/?',RESTfulHandler ),
                      ('/rooms/delete\/?',RoomRESTfulHandler ),
                      #('/tenants/?', RESTfulHandler)],
                      ('/tenants\/?', RESTfulHandler),
                      ('/rooms\/?', RoomRESTfulHandler)],
                      debug=True)

#def main():
#    run_wsgi_app(application)

#if __name__ == "__main__":
# main()


