"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from YearEndProject import app
from YearEndProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

import matplotlib.pyplot as plt

from matplotlib.figure import Figure

from YearEndProject.plot_service_functions import plot_to_img

from os import path

from flask_bootstrap import Bootstrap

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from YearEndProject.Models.QueryFormStructure import QueryFormStructure 
from YearEndProject.Models.QueryFormStructure import QueryFormStructure2
from YearEndProject.Models.QueryFormStructure import LoginFormStructure 
from YearEndProject.Models.QueryFormStructure import UserRegistrationFormStructure 

from YearEndProject.Models.QueryFormStructure import ExpandForm
from YearEndProject.Models.QueryFormStructure import CollapseForm
from YearEndProject.Models.LocalDatabaseRoutines import get_poketypes_choices

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

bootstrap = Bootstrap(app)


db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Project in data science',
        year=datetime.now().year,
        message='Project in data science'
    )

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page about pokemon',
        year=datetime.now().year,
        message='In this page we will display the dataset we are going to use in this project'
    )

@app.route('/DataSet1')
def DataSet1():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Pokemon.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')

    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
        title='This is Data Set 1 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the dataset we are using about pokemon.'
    )

@app.route('/Query', methods=['GET', 'POST'])
def Query():

    form = QueryFormStructure2(request.form)
    Name = ''
    Type1 = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Pokemon.csv'))
    df = df.set_index('Name')

    raw_data_table = df.to_html(classes = 'table table-hover')


    if (request.method == 'POST' ):
        name = form.name.data
        Pokemon = name
        if (name in df.index):
            Type1 = df.loc[name,'Type1']
            raw_data_table = ""
        else:
            Type1 = name + ', no such pokemon'
        form.name.data = ''


    """Renders the query page."""
    return render_template(
        'Query.html',
        form = form, 
        name = Type1,
        title='Project in data science',
        year=datetime.now().year,
        message='First type of a pokemon:'
    )

@app.route('/query2', methods=['GET', 'POST'])
def query2():

    form = QueryFormStructure2(request.form)
    Name = ''
    Type2 = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Pokemon.csv'))
    df = df.set_index('Name')

    raw_data_table = df.to_html(classes = 'table table-hover')


    if (request.method == 'POST' ):
        name = form.name.data
        Pokemon = name
        if (name in df.index):
            Type2 = df.loc[name,'Type2']
            raw_data_table = ""
        else:
            Type2 = name + ', no such pokemon'
        form.name.data = ''


    """Renders the query page."""
    return render_template(
        'Query2.html',
        form = form, 
        name = Type2,
        title='Project in data science',
        year=datetime.now().year,
        message='Second type of a pokemon:'
    )

@app.route('/query3', methods=['GET', 'POST'])
def query3():

    form = QueryFormStructure(request.form)
    form.poketypes.choices = get_poketypes_choices() 
    poketypes = ''
    chart = ''
    #select = ''
    if (request.method == 'POST' ):
        df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Types.csv'))
        df = df.set_index('type')
        types = form.poketypes.data
        df = df.loc[form.poketypes.data]
        #df = df.loc[['bug','dark','dragon','fairy','fighting','fire','flying','ghost','grass','ground','ice','normal','poison','psychic','rock','steel','water']]
        #df = df.rename(columns={'type': 'type'})
        df = df.transpose()
        df = df.reset_index()
        df = df.drop(['index'],1)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'bar')
        chart = plot_to_img(fig)

    

    return render_template(
        'Query3.html',
        img_under_construction = '/static/imgs/under_construction.png',
        chart = chart ,
        poketypes = poketypes ,
        form = form ,
        height = "300" ,
        width = "750"
    )
