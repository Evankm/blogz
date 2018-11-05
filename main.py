from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(120), nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content  

tasks = []
contents = []
titles = []
@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'GET':
        posts = Post.query.all()
    return render_template('todos.html', posts=posts)

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)
        posts = Post.query.all()

    return render_template('todos.html', title='tasks', tasks=tasks, posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])   
def newpost():
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        title = request.form['title']
        titles.append(title)
        content = request.form['content']
        post = Post(title, content)
        contents.append(content)

        if title == '':
            title_error = 'Please fill in title'
        else:
            title_error = ''  
        if content == '':
            blog_error = 'Please fill in blog'
        else:
            blog_error = '' 

        if title != '' and content != '':
            db.session.add(post)
            db.session.commit()
            return redirect('newestpost')
        else:
            return render_template('newpost.html',title=title, content=content, blog_error=blog_error, title_error=title_error)

            

    return render_template('newpost.html', title=title, content=content) 

@app.route('/post', methods=['POST', 'GET'])   
def post():
    if request.method == 'GET':
        post1 = request.args.get('id')
        post2 = Post.query.filter(Post.id == post1).first()
        return render_template('post.html', post1=post1, post=post, post2=post2)
 

@app.route('/newestpost', methods=['GET', 'POST'])
def post_page():
    post1 = [] 
    if request.method == 'GET':
        post = Post.query.all() 
    post2 = post[-1]
    
    return render_template('newestpost.html', post2 = post2)

if __name__=='__main__':
    app.run()
