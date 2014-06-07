import os
import urllib

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
        self.render_template('index.html',{'posts':post_query})

class PostHandler(BaseHandler):
    def post(self):
        post = Post(
            title=self.request.get('title'),
            content=self.request.get('content')
        )
        post.put()
        self.redirect('/')
        
class CreatePlace(BaseHandler):
    def get(self):
        place = Place(
            name='Google',
            location=ndb.GeoPt(lat=1.279,lon=103.85)
        )
        place.put()
        self.redirect('/')


class Upvote(BaseHandler):
    def get(self):
        post_id = int(self.request.get('id'))
        query = Post.get_by_id(post_id)
        query.rating += 1
        query.put()
        self.redirect('/')
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler),
    ('/debug', CreatePlace),
    ('/upvote', Upvote)
], debug=True)
