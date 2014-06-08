from google.appengine.ext import ndb

class Place(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty()

class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    author = ndb.StringProperty(default="Anonymous")
    img = ndb.BlobProperty()
    rating = ndb.IntegerProperty(default=0)
    place = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    comment = ndb.IntegerProperty(default=0)
    
class Comment(ndb.Model):
    post = ndb.KeyProperty(kind=Post)
    content = ndb.StringProperty()
    author = ndb.StringProperty(default="Anonymous")
    time = ndb.DateTimeProperty(auto_now_add=True)