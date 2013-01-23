"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators


class ChannelForm(wtf.Form):
    id = wtf.TextField('Id', validators=[validators.Required()])
    name = wtf.TextField('Name', validators=[validators.Required()])
    token = wtf.TextField('Token', validators=[validators.Required()])

class BotForm(wtf.Form):
    name = wtf.TextField('Name', validators=[validators.Required()])
    activated = wtf.BooleanField('Activated')
    code = wtf.TextAreaField('Code', validators=[validators.Required()])
