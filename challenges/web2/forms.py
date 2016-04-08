from flask.ext.wtf import Form, TextField, SubmitField

class DeadlinkForm(Form):
  Link = TextField("Link")
  submit = SubmitField("Send")
