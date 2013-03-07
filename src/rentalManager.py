from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from models import Tenants
from models import TenantList
from google.appengine.ext import db
#import simplejson
import django.utils.simplejson as json
from datetime import datetime


from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

from datetime import datetime
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
    def get(self, tenantId):
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
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(tenants)
    
    def post(self ):
        key = self.request.cookies['tenantlist']
#        tenantList = db.get(key)
#        tenant = simplejson.loads(self.request.body)
#        tenant = Tenants(tenantList = tenantList.key(),
#                 firstName   = tenant['FirstName'],
#                 surname   = tenant['Surname'],
#                 gender   = tenant['Gender'],
#                 age   = tenant['Age'],
#                 phoneNumber   = tenant['PhoneNumber'],
#                 email = tenant['Email'],
#                 registerDate = tenant['RegisterDate'])
#        tenant.put()
#        tenant = simplejson.dumps(tenant.toDict())
#        self.response.out.write(tenant)
    
        self.response.headers['Content-Type'] = 'application/json'
        jsonString = self.request.body          
        inputData = simplejson.loads(jsonString) #Decoding JSON 
#        Tenants().registerTenant(inputData,key) 
#        #tenant = Tenant().registerTenant(data)
#        #tenant.createRegisterActivityRecord()
#        tenantRegisterResponse = {'tenantRegisterMsg':'Congratulations, you have registered a new tenant successfully!'}
#        jsonResponse = simplejson.dumps(tenantRegisterResponse)
#        return self.response.out.write(jsonResponse)
        tenant = simplejson.dumps(Tenants().registerTenant(inputData,key))
        self.response.out.write(tenant)
    
    def put(self, tenantId):
        key = self.request.cookies['tenantlist']
        tenantlist = db.get(key)
        tenant = Tenants.get_by_id(int(tenantId))
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
        
        
application = webapp.WSGIApplication(
                     [('/', MainHandler),
                     #('/upload',UploadHandler),
                    #('/tenants',TenantHandler),
                      ('/tenants\/?([0-9]*)', RESTfulHandler)],
                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


