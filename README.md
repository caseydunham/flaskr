# flaskr ![Build Status](https://travis-ci.org/caseydunham/flaskr.svg?branch=master "Build Status") [![Coverage Status](https://coveralls.io/repos/github/caseydunham/flaskr/badge.svg?branch=master)](https://coveralls.io/github/caseydunham/flaskr?branch=master)

This is the flaskr application that is built as part of the 
[Flask tutorial](http://flask.pocoo.org/docs/0.11/tutorial/).

I'm currently using this as a testbed for building out flask applications.

## Running

1. Create a virtual environment and activate it:
    
    `$ mkproject flaskr`
    `$ workon flaskr`
  
2. Install dependencies

    `$ pip install -r requirements.txt`
    
3. Set Flask environment variables
   
     `$ export FLASK_APP=flaskr.py`
     
4. Initialize database

    `$ flask dbinit`
   
5. Run application

    `$ flask run`
    
Access application at localhost:5000
