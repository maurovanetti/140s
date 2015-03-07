import webapp2
import json
from db import *

def model_to_json(data_list):
    for d in data_list:
        return json.dumps(d.to_dict())

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


class Leggi(webapp2.RequestHandler):
    def get(self):
        users=User.user_by_id(ndb.Key("User",1))
        users=model_to_json(users)
        self.response.write(users)

class Scrivi(webapp2.RequestHandler):
    def get(self):
        id=1
        u=User(parent=ndb.Key("User",id),name="Pippo",pwd="pluto")
        u.put()

class new_track(webapp2.RequestHandler):
    def post(self):
        params=self.request.POST
        hashtag=params["hashtag"]
        author=params["author"]
        url=params["url"]
        t=Track(hashtag=hashtag,author=author,url=url)



application = webapp2.WSGIApplication([
    ('/newtrack', new_track),
    ('/scrivi', Scrivi),

], debug=True)