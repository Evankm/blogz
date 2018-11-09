from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:buildablog2@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'yW8`xt7S[&L#iP'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(120), nullable=False) 
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content 
        self.author = author 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        

contents = []
titles = []
@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash('logged in')
            return redirect('/')
        else:
            flash('User password incorect, or user does not exist', 'error')
           

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            if verify == password:
                if email != '':
                    if password != '':
                
                        new_user = User(email, password)
                        db.session.add(new_user)
                        db.session.commit()
                        session['email'] = email
                        return redirect('/')
                    else:
                        flash('Must create password', 'error')    
                else:
                     flash('Must create username', 'error')        
            else:
                flash('Verify password', 'error')
                
        else:
            flash('User already exists', 'error')
    return render_template('register.html')    

@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'GET':
        posts = Post.query.all()
    return render_template('todos.html', posts=posts)

    if request.method == 'POST':
        posts = Post.query.all()

    return render_template('todos.html', title='tasks', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])   
def newpost():
    author = User.query.filter_by(email=session['email']).first()

    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        title = request.form['title']
        titles.append(title)
        content = request.form['content']
        post = Post(title, content, author)
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
            my_posts = Post.query.filter_by(title=title, content=content, author=author).all()
            return redirect('newestpost')
        else:
            return render_template('newpost.html',title=title, content=content, blog_error=blog_error, title_error=title_error)

            

    return render_template('newpost.html', title=title, content=content) 
@app.route('/mypost', methods=['Post', 'GET']) 
def mypost():
    author = User.query.filter_by(email=session['email']).first()
    my_posts = Post.query.filter_by(author=author).all()
    if request.method == 'GET':
        post1 = request.args.get('id')
        post = Post.query.filter(Post.id == post1).first()
        return render_template('singleUser.html', my_posts=my_posts, post=post)

@app.route('/users', methods=['Post', 'GET']) 
def users():
    author = User.query.filter_by(email=session['email']).first()
    my_posts = Post.query.filter_by(author=author).all()
    if request.method == 'GET':
        users = User.query.all()
        return render_template('users.html', my_posts=my_posts, users=users)

@app.route('/others', methods=['POST', 'GET'])
def others():
    if request.method == 'GET':
        user = request.args.get('id')
        users_post = Post.query.filter(Post.author_id == user)
        post1 = request.args.get('id')
        post = Post.query.filter(Post.id == post1).first()
        return render_template('others.html', users_post=users_post, post=post)

@app.route('/post', methods=['POST', 'GET'])   
def post():
    if request.method == 'GET':
        post1 = request.args.get('id')
        post2 = Post.query.filter(Post.id == post1).first()
        users = Post.query.all()
        return render_template('post.html', post1=post1, post=post, post2=post2, users=users)
 

@app.route('/newestpost', methods=['GET', 'POST'])
def post_page():
    post1 = [] 
    if request.method == 'GET':
        post = Post.query.all() 
    post2 = post[-1]
    
    return render_template('newestpost.html', post2 = post2)

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

if __name__=='__main__':
    app.run()
