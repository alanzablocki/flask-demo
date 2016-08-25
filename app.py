from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
app = Flask(__name__)
#app.config.from_object(__name__)
#app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route('/')
def main():
    return redirect('/index')

@app.route("/index", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    print form.errors
    if request.method == 'POST':
        name=request.form['name'].upper()
        print name

        if form.validate():
	    return redirect('/success')
            #flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')  # render a template

if __name__ == "__main__":
    app.run(debug = False)
