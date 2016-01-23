import json
import requests
import plugins
from ghinfo import *
from links import *

def _initialise():
    plugins.register_admin_command(['issue'])

def issue(bot, event, *args):
    '''Create an issue on github.com using the given parameters.'''
    try:
        if args:
            url = 'https://api.github.com/repos/{}/{}/issues'.format(REPO_OWNER, REPO_NAME)
            
            if str(args[0]).isdigit():
                try:
                    num = int(args[0]) * -1
                    link = shorten(str(data[num][u'html_url']))
                    title = str(data[num][u'title'])
                    msg = _('{} -- {}').format(title, link)
                except:
                    msg = _('Invalid Issue Number')
            else:
                session = requests.Session()
                session.auth=(USERNAME, PASSWORD)
                # Create our issue
                issue = {'title': ' '.join(args),
                         'body': 'Issue created by {}'.format(event.user.full_name)}
                # Add the issue to our repository
                get = requests.get(url)
                data = json.loads(get.text)
                r = session.post(url, json.dumps(issue))
                link = shorten(str(data[0][u'html_url']))
                if r.status_code == 201:
                    msg = _('Successfully created issue: {}').format(link)
                else:
                    msg = _('Could not create issue.<br>Response: {}').format(r.content)

        else:
            msg = _('No issue given.')
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message('UgwEsRHkk27NK2sRISx4AaABAQ', msg)
