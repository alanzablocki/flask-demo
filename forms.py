from wtforms import Form, TextField, TextAreaField, StringField, SubmitField, BooleanField
from wtforms import validators, ValidationError
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    clPrice = BooleanField('Closing Price')
    adjclPrice = BooleanField('Adj. Closing Price')
    opPrice = BooleanField('Opening Price')
    adjopPrice = BooleanField('Adjusted Opening Price')

