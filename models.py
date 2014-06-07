from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    img = ndb.BlobProperty()
    rating = ndb.IntegerProperty()
    place = ndb.KeyProperty(kind=Place)
    time = ndb.DateTimeProperty(auto_now_add=True)

class Place(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    
class Comment(ndb.Model):
    post = ndb.KeyProperty(kind=Post)
    content = ndb.StringProperty()