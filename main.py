import os
import urllib

import jinja2
import webapp2

from models import Post as Feedback

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
        self.render_template('index.html',{})

class PostHandler(BaseHandler):
    def post(self):
        post = Feedback(
            title=self.request.get('title'),
            content=self.request.get('content'))
        post.put()
        self.redirect('/')
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler)
], debug=True)
