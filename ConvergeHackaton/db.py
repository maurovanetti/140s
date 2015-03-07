import cgi
import urllib

import webapp2

from google.appengine.ext import ndb

class User(ndb.Model):
    screen_name = ndb.StringProperty()
    @classmethod
    def user_by_id(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)


class Track:
    file_url=ndb.StringProperty()
    date=ndb.DateProperty()
    lenght=ndb.IntengerProperty()
    author=ndb.ReferenceProperty(User)
    hashtag=ndb.ReferenceProperty(Hashtag)

class Hashtag:
    text=ndb.StringProperty()
