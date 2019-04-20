from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysqul+pymysql://build-a-blog:success@localhost:8889/build-a-blog' #connection string that connects to database
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app) #This calls the SQLAlchemy constructor and we pass in flask app


tasks = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    return render_template('todos.html', title="Build a Blog", tasks=tasks)    




app.run()    