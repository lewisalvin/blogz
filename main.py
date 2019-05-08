from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:success@localhost:8889/blogz' #connection string that connects to database
app.config['SQLALCHEMY_ECHO'] = True #Displays sql query in command line

db = SQLAlchemy(app) #This calls the SQLAlchemy constructor and we pass in flask app
app.secret_key = 'otrII05032016'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) #makes connection between owner id and user id(primary key) in User table

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner') #makes relationship between blogs and Blog table owner id

    def __init__(self, username, password):
        self.username = username
        self.password = password
        




@app.route('/blog')
def home():
    blogs = Blog.query.all()
    id = request.args.get('id')
    userid = request.args.get('user')
    user_posts = User.query.filter_by(id=id).all
    if userid != None:
        blogs = Blog.query.filter_by(owner_id=userid).all()

    

    return render_template('blog.html', title="Build a Blog", blogs=blogs, user_posts=user_posts)    


@app.route('/')
def index():
    users = User.query.all()

    return render_template('index.html', users=users)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    title_blog = ""
    blog = ""
    blog_post = ""
    title_error = ""
    blog_error = ""
    
    if request.method == 'POST':
        owner = User.query.filter_by(username=session['username']).first()
        title_blog = request.form['title_blog']
        blog_post = request.form['blog']   
        

        if title_blog == "":
            title_error = "Please enter a title."
        if blog_post == "":
            blog_error = "Please enter a blog post."

    #if request.method == 'POST':
        if not title_error and not blog_error:
            new_entry = Blog(title_blog, blog_post, owner)
            db.session.add(new_entry)
            db.session.commit()
            x= new_entry.id
            #return redirect('/entry?id={}'.format(x))
            return render_template('entry.html', blog=new_entry, user=x)
        else:    
        #blogs = Blog.query.all()
            pass
    return render_template('new_post.html',title="Build a blog", title_blog=title_blog, blog=blog, title_error=title_error, blog_error=blog_error)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', '/']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')



@app.route('/entry')
def entry():
    #blogs = Blog.query.all()
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    user = User.query.filter_by(id=blog.owner_id).first()
    return render_template('entry.html', blog=blog, user=user)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verifyPassword']
        existing_user = User.query.filter_by(username=username).first()
        username_error = ''
        password_error = ''
        verifyPassword_error = ''
        # print(existing_user)
        # print(username)


        if len(username) == 0:
            username_error = 'Can not be blank'

        if len(password) == 0:
            password_error = 'Can not be blank'    

        if len(verify) == 0:
            verifyPassword_error = 'Can not be blank'

        if username == existing_user:
            username_error = 'Username already exists'

        if verify != password:
            password_error = 'both passwords must match'

        if len(password) < 3:
            password_error = 'can not be less than 3 characters' 

        if len(username) < 3:
            username_error = 'can not be less than 3 characters'                   

        if existing_user == None and not username_error and not password_error and not verifyPassword_error:
            # print("Jackass Python")
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')
        else:
            # print("Correct but busted")
            return render_template('signup.html', username=username, username_error=username_error, password_error=password_error, verifyPassword_error=verifyPassword_error)    


    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    username_error = ''
    password_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        #passw = User.query.filter_by(password=password).first
        if user and user.password == password:
            session['username'] = username
            return redirect('/blog')
        if not user:
            return render_template('login.html', username_error='Username does not exist')  
        else:
            return render_template('login.html', password_error='That password or username is incorrect.')  
            



    


    return render_template('login.html')

# @app.route('/index')
# def index():        
#     return render_template('index.html')



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()