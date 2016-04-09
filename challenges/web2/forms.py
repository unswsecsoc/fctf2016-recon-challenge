from flask.ext.wtf import Form
from wtforms.fields import TextField, SubmitField
from wtforms import validators
import index


class DeadlinkForm(Form):
  Link = TextField("Link", [
    validators.Regexp("^http:\/\/" + index.hostname + "/.*$")])
  submit = SubmitField("Send")
