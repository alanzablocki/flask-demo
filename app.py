from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField
import requests
import numpy as np
import pandas as pd
from bokeh.charts import Scatter
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.embed import components

# App config.
app = Flask(__name__)

app.config.from_object(__name__)				# removing next two lines does not
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'	# give you the Error messages

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    clPrice = BooleanField('Closing Price')
    adjclPrice = BooleanField('Adj. Closing Price')
    opPrice = BooleanField('Opening Price')
    adjopPrice = BooleanField('Adjusted Opening Price')


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    print form.errors
    if request.method == 'POST':
        name=request.form['name'].upper()
        if form.validate():
	    return redirect(url_for("graph", name=name))
	    #return redirect('/graph')
            #flash('Thanks for registration ' + name)
        else:
            flash('Error: Please enter a valid ticker symbol. ')
    return render_template('index.html', form=form)

@app.route('/graph/<name>', methods=['GET','POST']) # might have to add some stuff here!
def graph(name):

    stock_name = name # "AAPL" #name
    # get stock api
    url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock_name
    # select dates - future version

    # get the data

    # from tdi blog, slightly different than p171 in Pandas Wes McKinney
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(url)
    # json decode
    rd = raw_data.json()

    # create pandas data frame
    df = pd.DataFrame(rd['data'],columns=rd['column_names'])
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)

    p = figure(width=600, height=500, x_axis_type="datetime",x_axis_label="Date",\
    title=stock_name + " Stock", toolbar_location = "above") # , legend = 'top_left') # this throws an error
    p.line(df.index, df['Open'], color='green', legend='Opening Price')
    # p.legend.orientation = "top_left" # returns server error
    script, div = components(p)
    return render_template('graph.html', script=script, div=div) #, form=form) # added form=form

# debug page
#@app.route('/success')
#def success():
#    return render_template('success.html')  # render a template

if __name__ == "__main__":
  app.run(port=33507)
