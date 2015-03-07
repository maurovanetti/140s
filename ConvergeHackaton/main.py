import webapp2
import json
from db import *

def model_to_json(data_list,entity=True):
    def clean_entry(d):
        d=d.to_dict()
        d["date"]=str(d["date"])
        return d
    if entity:
        data_list=[clean_entry(d) for d in data_list]


    return json.dumps(data_list)

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
        hashtag_text=params["hashtag"]


        author=params["author"]

        file_url=params["file_url"]
        metadata_url=params["metadata_url"]
        t=Track(hashtag=hashtag_text,author=author,file_url=file_url,metadata_url=metadata_url)
        t.put()
        self.response.write("ok")

class new_user(webapp2.RequestHandler):
    def post(self):
        params=self.request.POST
        author=params["author"]
        u=User(author=author)
        u.put()
        self.response.write("ok")


class get_track_list(webapp2.RequestHandler):
    def post(self):
        hashtag=self.request.POST["hashtag"]
        t=Track.get_track_by_hashtag(hashtag,20)
        t=model_to_json(t)
        self.response.write(t)

class get_all_hashtag_list(webapp2.RequestHandler):
    def get(self):
        self.response.write(model_to_json(Track.get_all_hashtag()))


class get_hashtag_list(webapp2.RequestHandler):
    def post(self):
        size=self.request.POST["max_results"]
        h_list=Track.get_all_hashtag()
        self.response.write(h_list)
        fake_hashtags=["converge","milanroma","hackaton","JeSuisCharlie","Renzi",
                       "TuttiACasa","BersaglioMobile","Libia","Italia","MasterChef","IoStoConMorresi"]

        import random
        if(len(h_list)<5):
            res=random.sample(fake_hashtags,size)
        else:
            res=random.sample(h_list,size)
        output={"result":list(res)}
        self.response.write(model_to_json(output,entity=False))

class get_next_track(webapp2.RequestHandler):
    def post(self):
        hashtag=self.request.POST["hashtag"]

        t=Track.get_track_by_hashtag(hashtag,1)
        self.response.write(model_to_json(t))

class get_next_track_smart(webapp2.RequestHandler):
    def post(self):
        hashtag=self.request.POST["hashtag"]
        listener=self.request.POST["listener"]

        best=Track.get_track_by_hashtag(hashtag,100)
        listened=Listened.get_listened_by_listener(listener)
        for track in best:
            found = True
            for bad_track in listened:
                if track.file_url == listened.screen_name:
                    found = False
                else
                    found = True
                    break
            if found:
                l=Listened(file_url=track.file_url,screen_name=listener)
                l.put()
                self.response.write(model_to_json(track))
                return
            
        output={"success":False, "message":"Queue exhausted"}
        self.response.write(model_to_json(output))


application = webapp2.WSGIApplication([
    ('/newtrack', new_track),
    ('/newuser', new_user),
    ('/gettracklist', get_track_list),
    ('/nexttrack',get_next_track_smart),
    ('/hashtags', get_hashtag_list),

], debug=True)
