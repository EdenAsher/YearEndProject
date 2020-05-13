"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from YearEndProject import app
from YearEndProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from flask_bootstrap import Bootstrap

from YearEndProject.Models.LocalDatabaseRoutines import ExpandForm
from YearEndProject.Models.LocalDatabaseRoutines import CollapseForm

from flask import redirect, request

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
    return render_template(
        'index.html',
        title='Home Page',
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Project in data science',
        message='Project in data science'
    )

@app.route('/register', methods=['GET', 'POST'])
def Register():
    #register page
    form = UserRegistrationFormStructure(request.form)

    #Registers a new user, makes sure the username and password are original, adds the user to users.csv
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
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    #login page
    form = LoginFormStructure(request.form) #takes the form we created.

    if (request.method == 'POST' and form.validate()): #when the user clicks submit
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)): #checks that the login is "good"
            return redirect('query3') #takes the user to query3
        else:
            flash('Error in - Username and/or password') #if the login isn't good, it brings up an error.
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        repository_name='Pandas',
        )

@app.route('/DataModel')
def DataModel():
    """Renders the data model page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page about Pokémon',
    )

@app.route('/DataSet1', methods=['GET', 'POST'])
def DataSet1():

    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Pokemon.csv')) #Reads the csv
    raw_data_table = ''

    #Expand and collapse, sample randomizer.
    if (request.method == 'POST'): 
        if (request.form['action'] == 'Expand' and form1.validate_on_submit()):
            raw_data_table = df.sample(30).to_html(classes = 'table table-hover')
        if (request.form['action'] == 'Collapse' and form2.validate_on_submit()):
            raw_data_table = ''

    return render_template(
        'DataSet1.html',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2,
        title='This is Data Set 1 page',
        message='In this page we will display the dataset we are using about Pokémon.'
    )

@app.route('/DataSet2', methods=['GET', 'POST'])
def DataSet2():

    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Types.csv')) #Reads the csv
    raw_data_table = ''

    #Expand and collapse, sample randomizer.
    if (request.method == 'POST'):
        if (request.form['action'] == 'Expand' and form1.validate_on_submit()):
            raw_data_table = df.to_html(classes = 'table table-hover')
        if (request.form['action'] == 'Collapse' and form2.validate_on_submit()):
            raw_data_table = ''

    return render_template(
        'DataSet2.html',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2,
        title='This is Data Set 2 page',
        message='In this page we will display the dataset we are using about Pokémon.'
    )

@app.route('/Query', methods=['GET', 'POST'])
def Query():

    form = QueryFormStructure2(request.form) #gets the form we created in QueryFormStructure in models.
    Name = ''
    Type1 = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Pokemon.csv')) #reads the csv (data)
    df = df.set_index('Name')

    raw_data_table = df.to_html(classes = 'table table-hover')

    #Checks if the pokemon exists and than if it is, returns its type.
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
        message='First type of a pokemon:'
    )


@app.route('/query2', methods=['GET', 'POST'])
def query2():

    form = QueryFormStructure2(request.form) #gets the form we created in QueryFormStructure in models.
    Name = ''
    Type2 = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Pokemon.csv')) #reads csv (data)
    df = df.set_index('Name')

    raw_data_table = df.to_html(classes = 'table table-hover')

    #Checks if the pokemon exists and than if it is, returns its second type.
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
        message='Second type of a pokemon:'
    )

@app.route('/query3', methods=['GET', 'POST'])
def query3():

    form = QueryFormStructure(request.form) #gets the form we created in QueryFormStructure in models.
    form.poketypes.choices = get_poketypes_choices() #lets us use what we created in LocalDatabaseRoutines
    poketypes = ''
    chart = ''
    if (request.method == 'POST' ):
        df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\Types.csv')) #reads data
        df = df.set_index('type') #sets the index to "type"
        types = form.poketypes.data
        df = df.loc[form.poketypes.data] #makes it that it only gets what the user selected
        df = df.transpose()#changes rows to colums and vice versa, we use this to organize things so it's easier to use.
        df = df.reset_index()
        df = df.drop(['index'],1) #drops what we don't need

        #the following 4 lines render the actual graph
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'bar')
        chart = plot_to_img(fig)

    

    return render_template(
        'Query3.html',
        img_under_construction = '/static/imgs/under_construction.png',#part of creating the graph
        chart = chart ,
        poketypes = poketypes ,
        form = form ,
        height = "300" ,
        width = "750"
    )
