#coding=utf-8
import os
import sys
import logging
import re
import urllib, hashlib
import simplejson as json


from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import Request
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from model import Topic,Vote,UserAnswer,UserSeen,UserAnswerCount

SYSTEM_VERSION = '1.0.6'

def json_output(status, data={}):
    return json.dumps({'status': status, 'content': data})

def get_gravatar(email):
    return "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?s=36"

class BaseHandler(webapp.RequestHandler):

    @property
    def is_dev(self):
        return self.request.remote_addr == '127.0.0.1'

    @property
    def is_ajax(self):
        if 'X-Requested-With' in self.request.headers:
            return self.request.headers['X-Requested-With'] == 'XMLHttpRequest'

    @property
    def is_mobi(self):
        user_agent = self.request.headers['User-Agent']
        if (re.search('iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP', user_agent)):
            return True
        return False

    def render_index(self, type='latest', data = {}):
        page = int(self.request.get('page', 1))
        offset = (page - 1) * 15
        topic = Topic.all()
        if type == 'latest':
            topic.order('-date')
        elif type == 'top':
            topic.order('-voteup')
            topic.order('votedown')
        list = topic.fetch(limit=15, offset=offset)

        uac = UserAnswerCount()
        result = uac.getTop()

        topuser = []
        for item in result:
            topuser.append({
                'gravatar': get_gravatar(item.user.email()),
                'name': item.user.nickname(),
                'count': item.count,
            })

        tpl = 'index'
        if self.is_ajax:
            tpl = 'topic_list'
        default_data = {'list': list, 'page': page+1, 'list_length': len(list), 'topuser': topuser }
        data.update(default_data)
        self.render(tpl, data)

    def render(self, tpl, values = {}):
        user = users.get_current_user()
        values['is_dev'] = self.is_dev;
        values['system_version'] = SYSTEM_VERSION
        if user:
            values['user'] = {
                'logged_in': True,
                'nickname': user.nickname(),
                'logout_url': users.create_logout_url('/'),
                'is_admin': users.is_current_user_admin(),
            }
        else:
            values['user'] = {
                'is_admin': False,
                'logged_in': False,
                'login_url': users.create_login_url('/'),
            }

        if self.is_mobi:
            tpl += '.mobi'

        if not self.is_ajax:
            path = os.path.join('tpl', tpl + '.html')
            output = template.render(path, values)
            self.response.out.write(output)
        else:
            path = os.path.join('tpl', tpl + '.tpl')
            output = template.render(path, values)
            self.response.out.write(json_output('ok', {'html': output}))
        return


class MainPage(BaseHandler):
    def get(self):
        self.render_index('latest')

class SentenceHandler(BaseHandler):
    def post(self):
        if (not self.request.get('sentence')):
            self.response.out.write(json_output('error', {
                'message': 'empty sentence',
            }))
            return
        if (not self.request.get('answer')):
            self.response.out.write(json_output('error', {
                'message': 'empty answer',
            }))
            return

        topic = Topic()
        topic.author = users.get_current_user()
        topic.sentence = self.request.get('sentence')[:300]
        topic.answer = self.request.get('answer')
        topic.put()
        self.response.out.write(json_output('ok', {
            'user': topic.author.nickname(),
            'sentence': topic.sentence,
            'answer': topic.answer,
        }))

class VoteHandler(BaseHandler):        
    def post(self):
        topic = Topic.get(self.request.get('entity'))
        if int(self.request.get('mark')) != 1:
            if not topic.votedown:
                topic.votedown = -1
            else:
                topic.votedown -= 1
        else:
            if not topic.voteup:
                topic.voteup = 1
            else:
                topic.voteup += 1
        topic.put()

        vote = Vote()
        vote.author = users.get_current_user()
        vote.topic = topic
        vote.mark = int(self.request.get('mark'))
        vote.put()

        self.response.out.write(json_output('ok'))

class TopHandler(BaseHandler):
    def get(self):
        self.render_index('top')

class DelHandler(BaseHandler):
    def get(self):
        topic = Topic.get(self.request.get('key').strip()).delete()
        self.redirect('/')

class GuessHandler(BaseHandler):
    def post(self):
        topic = Topic.get_by_id(int(self.request.get('id')))
        if not topic:
            self.response.out.write('莫有找到台词~~~')
            return

        user = users.get_current_user()
        if topic.answer == self.request.get('answer'):
            if user:
                ua = UserAnswer()
                ua.user = user
                ua.topic = topic
                ua.put()

                uac = UserAnswerCount.all()
                uac.filter('user =', user)
                result = uac.get()
                if result.count:
                    result.count += 1
                else:
                    result.count = 1
                result.put()
            self.response.out.write(json_output('ok', {'message': '答对了，不错哦'}))
            return
        self.response.out.write(json_output('fail', {'message': '再想想？'}))

class ViewAnswerHandler(BaseHandler):
    def get(self):
        topic = Topic.get_by_id(int(self.request.get('id')))
        if not topic:
            self.response.out.write('莫有找到台词~~~')
            return

        user = users.get_current_user()
        if user:
            ua = UserSeen()
            ua.user = user
            ua.topic = topic
            ua.put()
            self.response.out.write(json_output('ok', {'message': topic.answer}))
            return
        self.response.out.write('登录后就能看到答案了');
        

application = webapp.WSGIApplication(
	[('/', MainPage),
     ('/publish', SentenceHandler),
     ('/vote', VoteHandler),
     ('/top', TopHandler),
     ('/del', DelHandler),
     ('/guess', GuessHandler),
     ('/getanswer', ViewAnswerHandler),
		],
	debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

