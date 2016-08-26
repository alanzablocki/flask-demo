from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import numpy as np
import pandas as pd
from bokeh.charts import Scatter
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.embed import components

# App config.
app = Flask(__name__)
#app.config.from_object(__name__)
#app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

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
        print name

        if form.validate():
	    return redirect('/graph')
            #flash('Thanks for registration ' + name)
        else:
            flash('Error: Please enter a valid ticker symbol. ')
    return render_template('index.html', form=form)

@app.route('/graph', methods=['GET','POST']) # might have to add some stuff here!
def graph():
    stock_name = "AAPL" #a name
    # 2 get stock api
    url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock_name
    # select dates

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

    p = figure(width=400, height=300, x_axis_type="datetime",x_axis_label="Date",title=stock_name + " Stock")
    p.line(df.index, df['Open'], color='green', legend='Opening Price')
    
    script, div = components(p)
    return render_template('graph.html', script=script, div=div) #, form=form) # added form=form

# debug page
#@app.route('/success')
#def success():
#    return render_template('success.html')  # render a template

if __name__ == "__main__":
  app.run(port=33507)
#    app.run(debug = False)
