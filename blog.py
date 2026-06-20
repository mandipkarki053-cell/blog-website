from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'mandiphero123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blog.db')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    author = db.Column(db.String(80))


with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return '<p>Registered!</p>'
    else:
        return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Login successful!')
            return redirect('/')
        else:
            flash('Incorrect password!')
            return render_template('log.html')
    else:
        return render_template('log.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    posts = Post.query.all()
    return render_template('homepge.html', posts=posts)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content,
                        author=session['username'])
        db.session.add(new_post)
        db.session.commit()
        flash('Post Created')
        return redirect('/')
    else:
        return render_template('create.html')


@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get(id)
    if post:
        return render_template('post.html', post=post)
    else:
        return '<h1>Post not found!</h1>'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
