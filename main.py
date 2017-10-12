from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:deadlands@localhost:8889/build-a-blog'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    
    def __init__(self,title,date_posted,content):
        self.title = title
        self.date_posted = date_posted
        self.content = content

            

@app.route('/')
def index():

    return render_template('blog.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/blog')
def blog():
    posts = Blog.query.order_by(Blog.date_posted.desc()).all()

    return render_template('blog.html', posts=posts,)
@app.route('/blog<id>')
def post(id):
    post = Blog.query.get(id)
    return render_template('post.html', post=post)

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    check = 0
    error1= ""
    error2= ""
    if request.method == 'POST':           
        title = request.form['title']
        content = request.form['content']
        if len(title)<1:
           error1 = "Put a Title In There!"
           check +=1
        if len(content)<1:
            error2= "Write Something!"  
            check +=1
        if check >= 1:
            return render_template("add.html", error1=error1,error2=error2)
        else: 
            post = Blog(title=title,content=content, date_posted=datetime.now())
            db.session.add(post)
            db.session.commit()

        return redirect(url_for('blog'))
    

if __name__ == '__main__':
    app.run(debug=True)