from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from models import Tenants
from models import TenantList
from google.appengine.ext import db
import simplejson
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
        if self.request.cookies.get('tenants', None) == None:
            tenantList = TenantList()
            tenantList.put()
            cookie = Cookie.SimpleCookie()
            cookie['tenants'] = tenantList.key().__str__()
            cookie['tenants']['expires'] = datetime(2014, 1, 1).strftime('%a, %d %b %Y %H:%M:%S')
            cookie['tenants']['path'] = '/'
            self.response.headers.add_header('Set-Cookie', cookie['tenants'].OutputString())
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class RESTfulHandler(webapp.RequestHandler):
    def get(self, id):
        key = self.request.cookies['tenants']
        tenantList = db.get(key)
        tenants = []
        #query = Tenants.all()
        query = db.GqlQuery("SELECT * FROM Tenants")
        #query.filter("tenantList =", tenantList.key())
        for tenant in query:
            tenants.append(tenant.toDict())
        tenants = simplejson.dumps(tenants)
        self.response.out.write(tenants)
    
    def post(self, id):
        key = self.request.cookies['tenants']
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
        Tenants().registerTenant(inputData,key) 
        #tenant = Tenant().registerTenant(data)
        #tenant.createRegisterActivityRecord()
        tenantRegisterResponse = {'tenantRegisterMsg':'Congratulations, you have registered a new tenant successfully!'}
        jsonResponse = simplejson.dumps(tenantRegisterResponse)
        return self.response.out.write(jsonResponse)
    
    def put(self, id):
        key = self.request.cookies['tenants']
        tenantList = db.get(key)
        tenant = Tenants.get_by_id(int(id))
        if tenant.tenantList.key() == tenantList.key():
            tmp = simplejson.loads(self.request.body)
            tenant.content = tmp['content']
            tenant.done    = tmp['done']
            tenant.put()
            tenant = simplejson.dumps(tenant.toDict())
            self.response.out.write(tenant)
        else:
            self.error(403)
    
    def delete(self, id):
        key = self.request.cookies['tenants']
        tenantList = db.get(key)
        tenant = Tenants.get_by_id(int(id))
        if tenant.tenantList.key() == tenantList.key():
            tmp = tenant.toDict()
            tenant.delete()
        else:
            self.error(403)
    
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
        
        
application = webapp.WSGIApplication(
                     [('/', MainHandler),
#                      ('/tenants',TenantHandler),
                      ('/tenants\/?([0-9]*)', RESTfulHandler)],
                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


