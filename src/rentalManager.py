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
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Tenants
from models import TenantList
from google.appengine.ext import db
from datetime import datetime
from google.appengine.ext.webapp import template
from django.utils import simplejson
import os, Cookie

class MainHandler(webapp.RequestHandler):
    def get(self):
        if self.request.cookies.get('tenantlist', None) == None:
            tenantList = TenantList()
            tenantList.put()
            cookie = Cookie.SimpleCookie()
            cookie['tenantlist'] = tenantList.key().__str__()
            cookie['tenantlist']['expires'] = datetime(2014, 1, 1).strftime('%a, %d %b %Y %H:%M:%S')
            cookie['tenantlist']['path'] = '/'
            self.response.headers.add_header('Set-Cookie', cookie['tenantlist'].OutputString())
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class RESTfulHandler(webapp.RequestHandler):
    #def get(self, tenantId):
    def get(self):
        key = self.request.cookies['tenantlist']
        tenantlist = db.get(key)
        tenants = []
        query = Tenants.all()
        #query = db.GqlQuery("SELECT * FROM Tenants")
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
        
    def delete(self, tenantId):
        key = self.request.cookies['tenantlist']
        tenantlist = db.get(key)
        tenant = Tenants.get_by_id(int(tenantId))
        if tenant.tenantlist.key() == tenantlist.key():
            #tmp = tenant.toDict()
            tenant.delete()
        else:
            self.error(403)
        #self.response.out.write()
        
class TenantHandler(webapp.RequestHandler):
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

class UploadHandler(webapp.RequestHandler):     
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

class GetImage(webapp.RequestHandler):
    def get(self):
        tenant_id = self.request.get("tenant_id")
        tenant = db.get(tenant_id)
        if tenant.picture:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(tenant.picture)
            #self.response.out.write(tenant.firstName)
        else:
            self.response.out.write("no image for this tenant")
    
application = webapp.WSGIApplication(
                     [('/', MainHandler),
                     ('/uploadPicture',UploadHandler),
                    #('/tenants',TenantHandler),
                     ('/image',GetImage),
                     #('/tenants\/?([0-9]*)', RESTfulHandler)],
                      ('/tenants/update',RESTfulHandler ),
                      #('/tenants/?', RESTfulHandler)],
                      ('/tenants\/?', RESTfulHandler)],
                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


