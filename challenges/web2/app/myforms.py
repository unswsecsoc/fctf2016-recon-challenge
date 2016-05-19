from flask.ext.wtf import Form
from wtforms.fields import TextField, SubmitField
from wtforms import validators
from app import hostname

class DeadlinkForm(Form):
  Link = TextField("Link", [
    validators.Regexp("^http:\/\/" + hostname + "/.*$")])
  submit = SubmitField("Send")
