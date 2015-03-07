import cgi
import urllib

import webapp2

from google.appengine.ext import ndb

class User(ndb.Model):
    screen_name = ndb.StringProperty()
    @classmethod
    def user_by_name(cls, screen_name):
        return cls.query(User.screen_name==screen_name).fetch(1)


class Hashtag(ndb.Model):
    text=ndb.StringProperty()
    @classmethod
    def get_hashtag_by_text(cls,text):
        return cls.query(Hashtag.text==text).fetch(1)

class Track(ndb.Model):
    file_url=ndb.StringProperty()
    metadata_url=ndb.StringProperty()
    date=ndb.DateProperty(auto_now_add=True)
    length=ndb.IntegerProperty()
    author=ndb.StringProperty()
    score=ndb.IntegerProperty(default=1)
    hashtag=ndb.StringProperty()
    
    @classmethod
    def get_track_by_author(cls,author):
         return cls.query(Track.author==author).fetch(1)

    @classmethod
    def get_track_by_hashtag(cls,hashtag,amount):
         return cls.query(Track.hashtag==hashtag).order(-Track.date).fetch(amount)
    @classmethod
    def get_all_hashtag(cls):

       all_reg=cls.query().fetch(100)
       hashtags=set([r.hashtag for r in all_reg])
       return hashtags
