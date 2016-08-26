from flask import Flask, render_template, request, redirect, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests
import numpy as np
import pandas as pd
from bokeh.charts import Scatter
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.embed import components
#import matplotlib.pyplot as plt 


# define functions and classes

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    stock_name = TextField('Name:', validators=[validators.required()])

@app.route('/')
def main():
  return redirect('/index')    # redirect to index page

@app.route('/index',methods=['GET','POST']) # might have to add some stuff here!
def index():
    # not sure what goes here yet
    return redirect('/graph') #otherwise, go to the graph page
    #return render_template('index.html',form=form) #if request method was GET
    
    #return render_template('index.html')

# probably do 
@app.route('/graph',methods=['GET','POST']) # might have to add some stuff here!
def graph():
    #return render_template('index.html')

    form = ReusableForm(request.form)
    print form.errors
    if request.method == 'POST':
        stock_name=request.form['stock_name']
        print stock_name
        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')

    #return render_template('hello.html', form=form)     

    # 1 select stock to view
    # stock_name = "AAPL"
    # not used if our for works...
    
    # 2 get stock api
    url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock_name
    # select dates
    # get the data

    # from tdi blog, slightly different than p171 in Pandas Wes McKinney
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(url)

    # raw_data.raise_for_status() or .status_code
    # print "status code: " + str(raw_data.status_code)

    # json decode
    rd = raw_data.json()

    # create pandas data frame
    df = pd.DataFrame(rd['data'],columns=rd['column_names'])
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)

    #output_notebook()
    p = figure(width=400, height=300, x_axis_type="datetime",x_axis_label="Date",title=stock_name + " Stock")
    p.line(df.index, df['Open'], color='green', legend='Opening Price')
    #show(p)
    script, div = components(p)
    return render_template('graph.html', script=script, div=div, form=form) # added form=form

if __name__ == '__main__':
  app.run(port=33507)
  #app.run(host='0.0.0.0')
