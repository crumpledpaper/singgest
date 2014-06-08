import os
import urllib
import datetime

import jinja2
import webapp2

from models import Post, Place, Comment
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def post_key(post_name=None):
  """Constructs a Datastore key for a Post entity"""
  return ndb.Key('Post', post_name or '*notitle*')

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = JINJA_ENVIRONMENT.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainHandler(BaseHandler):
    def get(self):
        post_query = Post.query().order(-Post.time).fetch()
        place_query = Place.query().fetch()
        time = None
        for post in post_query:
            time = post.time.strftime("%a %d-%b-%Y %H:%M")
        self.render_template('index.html',{'posts':post_query, 'time':time, 'places': place_query})

class PostHandler(BaseHandler):
    def get(self):
        post = Post(
            title=self.request.get('title'),
            content=self.request.get('content'),
            place=self.request.get('place')
        )
        post.put()

class Upvote(BaseHandler):
    def get(self):
        post_id = int(self.request.get('id'))
        query = Post.get_by_id(post_id)
        query.rating += 1
        rating = query.rating
        query.put()
        self.response.out.write(rating)

class CreateComment(BaseHandler):
    def get(self):
        post_id = int(self.request.get('id'))
        post = Post.get_by_id(post_id)
        post.comment += 1
        post.put()
        comment = Comment(post=post.key, content=self.request.get("content"))
        comment.put()

class GetComment(BaseHandler):
    def get(self):
        post_id = int(self.request.get('id'))
        post = Post.get_by_id(post_id)
        comment_query = Comment.query().filter(Comment.post==post.key).order(-Comment.time).fetch()
        output = ''
        for comment in comment_query:
            output += '<div class="ui-bar ui-bar-a"><h3>'
            output += comment.author
            output += ' said...</h3></div>'
            output += '<div class="ui-body ui-body-a"><p>'
            output += comment.content
            output += '</p></div><br>'
        self.response.out.write(output)

class CreatePlace(BaseHandler):
    def get(self):
        name = self.request.get("name")
        place_query = Place.query().filter(name==name).fetch()
        if not place_query:
            place = Place(name=name)
            place.put()

class GetPlace(BaseHandler):
    def get(self):
        name = self.request.get("name")
        place_query = Place.query().filter(Place.name==name).fetch()
        key = place_query[0].key
        post_query = Post.query().filter(Post.place==key).fetch()
        
class GetPost(BaseHandler):
    def get(self):
        post_query = Post.query().fetch()
        output = []
        for post in post_query:
            place_query = Place.query().filter(Place.name==post.place).fetch()
            location = place_query[0].location
            output.append((post.place,location.lat,location.lon,post.rating))
        output = str(output)[2:-2]
        self.response.out.write(output)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler),
    ('/upvote', Upvote),
    ('/comment', CreateComment),
    ('/getcomment', GetComment),
    ('/createplace', CreatePlace),
    ('/getplace', GetPlace),
    ('/getpost', GetPost)
], debug=True)
