from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    clPrice = BooleanField('Closing Price')
    adjclPrice = BooleanField('Adj. Closing Price')
    opPrice = BooleanField('Opening Price')
    adjopPrice = BooleanField('Adjusted Opening Price')

