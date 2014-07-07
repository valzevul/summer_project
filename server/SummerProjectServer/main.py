__author__ = 'AlZimin'

#from flask import Flask
from flask import *
app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "HiS"

@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
  <head>
  <style type="text/css">
  body {
    color: purple;
    background-color: #e8e8e8 }

    button{
    width: 100px;
    height: 200px;
    font-size: 200%;
    background-color: #e8e8e8
}

  </style>
    <title>Admin page</title>
  </head>
  <body>
  <button type="button">+</button>
  <button type="button">-</button>
  </body>
</html>
'''

if __name__ == "__main__":
    app.run( debug = True )