from google.appengine.ext import ndb

class Place(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty()

class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    img = ndb.BlobProperty()
    rating = ndb.IntegerProperty(default=0)
    place = ndb.KeyProperty(kind=Place)
    time = ndb.DateTimeProperty(auto_now_add=True)
    
class Comment(ndb.Model):
    post = ndb.KeyProperty(kind=Post)
    content = ndb.StringProperty()