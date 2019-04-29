from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:success@localhost:8889/build-a-blog' #connection string that connects to database
app.config['SQLALCHEMY_ECHO'] = True #Displays sql query in command line

db = SQLAlchemy(app) #This calls the SQLAlchemy constructor and we pass in flask app

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

        




@app.route('/blog')
def index():
    blogs = Blog.query.all()
    

    return render_template('blog.html', title="Build a Blog", blogs=blogs)    

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    title_blog = ""
    blog = ""
    blog_post = ""
    title_error = ""
    blog_error = ""
    
    if request.method == 'POST':
        title_blog = request.form['title_blog']
        blog_post = request.form['blog']       

        if title_blog == "":
            title_error = "Please enter a title."
        if blog_post == "":
            blog_error = "Please enter a blog post."

    #if request.method == 'POST':
        if not title_error and not blog_error:
            new_entry = Blog(title_blog, blog_post)
            db.session.add(new_entry)
            db.session.commit()
            x= new_entry.id
            #return redirect('/entry?id={}'.format(x))
            return render_template('entry.html', blogs=new_entry)
        else:    
        #blogs = Blog.query.all()
            pass
    return render_template('new_post.html',title="Build a blog", title_blog=title_blog, blog=blog, title_error=title_error, blog_error=blog_error)




@app.route('/entry')
def entry():
    #blogs = Blog.query.all()
    id = request.args.get('id')
    blogs = Blog.query.filter_by(id=id).first()
    return render_template('entry.html', blogs=blogs)

    




if __name__ == '__main__':
    app.run()    