#coding=utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

import logging
import re
import hashlib
import simplejson as json

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from model import Topic,Vote,UserAnswer,UserSeen,UserAnswerCount

SYSTEM_VERSION = '1.1.0'
ITEMS_PER_PAGE = 15
SIMULATE_MOBILE = True

def json_output(status, data={}):
    return json.dumps({'status': status, 'content': data})

def get_gravatar(email):
    return "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?s=36"

class BaseHandler(webapp.RequestHandler):

    @property
    def is_ajax(self):
        if 'X-Requested-With' in self.request.headers:
            return self.request.headers['X-Requested-With'] == 'XMLHttpRequest'

    @property
    def is_mobi(self):
        user_agent = self.request.headers['User-Agent']
        if (re.search('iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP', user_agent)) or SIMULATE_MOBILE:
            return True
        return False

    def get_render(self, tpl, data = {}):
        if self.is_mobi:
            tpl += '.mobi'

        data['system_version'] = SYSTEM_VERSION
        user = users.get_current_user()
        data['user'] = {}
        if user:
            data['user']['logout_url'] = users.create_logout_url('/')
            data['user']['nickname'] = user.nickname()
            data['user']['logged_in'] = True
        else:
            data['user']['login_url'] = users.create_login_url('/')
            data['user']['logged_in'] = False
        data['items_per_page'] = ITEMS_PER_PAGE

        path = os.path.join('tpl', tpl + '.tpl')
        return template.render(path, data)
    
    def get_render_top_user(self):
        cache = memcache.get('top_user')
        if not cache:
            uac = UserAnswerCount()
            result = uac.getTop()

            topuser = []
            for item in result:
                topuser.append({
                    'gravatar': get_gravatar(item.user.email()),
                    'name': item.user.nickname(),
                    'count': item.count,
                })

            data = {'topuser': topuser }
            cache = self.get_render('top_user', data)
            memcache.set('top_user', cache, 60)
        return cache

    def get_render_topic_list(self, list_type='latest'):
        page = int(self.request.get('page', 1))

        user = users.get_current_user()
        user_key = user.user_id() if user else 'guest'
        topic_list = memcache.get('topic_list::'+list_type+'::'+user_key)

        if not topic_list or page != 1:
            offset = (page - 1) * ITEMS_PER_PAGE
            topic = Topic.all()
            if list_type == 'latest':
                topic.order('-date')
            elif list_type == 'top':
                topic.order('-voteup')
                topic.order('votedown')
            topic_list = topic.fetch(limit=ITEMS_PER_PAGE, offset=offset)

        if page == 1:
            if type == 'top':
                memcache.set('topic_list::top::'+user_key, topic_list, 1800)
            else:
                memcache.set('topic_list::latest::'+user_key, topic_list, 60)

        return self.get_render('topic_list', {'list': topic_list, 'list_length': len(topic_list), 'page': page+1})

    def render(self, tpl, values = {}):
        self.response.out.write(self.get_render(tpl, values))
        return

class MainPage(BaseHandler):
    def get(self):
        if not self.is_ajax:
            data = {'topic_list': self.get_render_topic_list('latest')}
            if not self.is_mobi:
                data['top_user'] = self.get_render_top_user()

            self.render('index', data)
        else:
            self.response.out.write(json_output('ok', {'html': self.get_render_topic_list('latest')}))

class TopHandler(BaseHandler):
    def get(self):
        if not self.is_ajax:
            self.render('index', {
                'topic_list': self.get_render_topic_list('top'),
                'top_user': self.get_render_top_user(),
                })
        else:
            self.response.out.write(json_output('ok', {'html': self.get_render_topic_list('top')}))

class SentenceHandler(BaseHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.response.out.write('~!@#$%')
            return

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

        memcache.delete('topic_list::latest'+user.user_id())

        if self.is_ajax:
            self.response.out.write(json_output('ok', {
                'user': topic.author.nickname(),
                'sentence': topic.sentence,
                'answer': topic.answer,
            }))
        else:
            self.redirect('/')

class VoteHandler(BaseHandler):        
    def post(self):
        user = users.get_current_user()
        if not user:
            self.response.out.write('~!@#$%')
            return

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

        memcache.delete('topic_list::latest'+user.user_id())
        self.response.out.write(json_output('ok'))

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
                if result:
                    result.count += 1
                    result.put()
                else:
                    uac = UserAnswerCount()
                    uac.user = user
                    uac.count = 1
                    uac.put()
                memcache.delete('topic_list::latest'+user.user_id())

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
            memcache.delete('topic_list::latest'+user.user_id())
            self.response.out.write(json_output('ok', {'message': topic.answer}))
            return
        self.response.out.write('登录后就能看到答案了');
        

application = webapp.WSGIApplication(
	[('/', MainPage),
     ('/publish', SentenceHandler),
     ('/vote', VoteHandler),
     ('/top', TopHandler),
     ('/guess', GuessHandler),
     ('/getanswer', ViewAnswerHandler),
		],
	debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

