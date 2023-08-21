from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/instagram'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'aaaa'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg', 'mp4'}


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    password = Column(String)
    gmail = Column(String)
    bio = Column(String)
    photo = Column(String)
    admin = Column(Boolean)
    reels = db.relationship("Reels", backref="users", secondary="save", order_by="Reels.id")
    like = relationship("Reels", backref="liked_by", secondary="like", order_by="Reels.id")
    follow = relationship("Follow", backref='users', order_by="Follow.id")
    comment_user = relationship("Comment", backref='users', order_by="Comment.id")

    def __repr__(self):
        return f'{self.id}'


class Follow(db.Model):
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    following_id = Column(Integer)


class Reels(db.Model):
    __tablename__ = 'reels'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    photo = Column(String)
    sound = Column(String)
    reel = Column(String)
    reel_name = Column(String)
    caption = Column(String)
    location = Column(String)
    like = Column(Integer)
    length_comment = Column(Integer)
    comment_reel = db.relationship('Comment', backref='reels', order_by="Comment.id")

    def __repr__(self):
        return f'{self.id}'


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    reel_id = Column(Integer, ForeignKey('reels.id'))
    text = Column(String)


db.Table('like',
         db.Column('reel_id', db.Integer, db.ForeignKey('reels.id')),
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

db.Table('save',
         db.Column('reel_id', db.Integer, db.ForeignKey('reels.id')),
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')))


def current_user():
    user_now = None
    if 'username' in session:
        user_get = Users.query.filter(Users.username == session['username']).first()
        user_now = user_get

    return user_now


def users_folder():
    upload_folder = 'static/img/'
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
    return value and type_file


@app.route('/', methods=["POST", "GET"])
def hello_world():
    user = current_user()
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        username = Users.query.filter(Users.username == name).first()
        if username:
            if check_password_hash(username.password, password):
                session["username"] = username.username
                return redirect(url_for('edit', user=user))
            else:
                return render_template('login.html', error='Username or password incorect')
    return render_template('login.html')


@app.route('/reg', methods=["POST", "GET"])
def reg():
    if request.method == "POST":
        name = request.form.get('name')
        usernames = request.form.get('username')
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        username = Users.query.filter(Users.username == usernames).first()
        if username:
            return render_template('reg.html', eror="This username already used")
        else:
            hashed = generate_password_hash(password=password, method='sha256')
            add = Users(name=name, password=hashed, username=usernames,
                        gmail=gmail, photo='static/img/1.jpg')
            db.session.add(add)
            db.session.commit()

            return redirect(url_for('reg'))
    return render_template('reg.html')


@app.route('/index')
def index():
    user = current_user()
    reels = Reels.query.join(Users, Reels.user == Users.id) \
        .join(Follow, Follow.follower_id == Users.id) \
        .filter(Follow.following_id == user.id) \
        .order_by(Reels.id) \
        .all()
    print(user.comment_user)
    filter = Users.query.filter(Users.id == user.id).first()
    save = filter.reels
    like = filter.like
    follow = Follow.query.filter(Follow.following_id == user.id).all()
    users = Users.query.all()
    return render_template('index.html', user=user, shahzod=reels, follow=follow, users=users, save=save, like=like)


@app.route('/add_comment/<int:id>', methods=['POST', 'GET'])
def add_comment(id):
    user = current_user()
    if request.method == "POST":
        comments = request.form.get('comment')
        filter = Reels.query.filter(Reels.id == id).first()
        soni = filter.length_comment
        add = Comment(text=comments, reel_id=id, user_id=user.id)
        db.session.add(add)
        db.session.commit()
        Reels.query.filter(Reels.id == id).update({
            'length_comment': soni + 1
        })
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_like/<int:id>')
def add_like(id):
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == session['username']).first()
    user_now.like.append(post_now)
    like_user = post_now.like + 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/dislike/<int:id>')
def dislike(id):
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == session['username']).first()
    user_now.like.remove(post_now)
    like_user = post_now.like - 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_likee/<int:id>')
def add_likee(id):
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == session['username']).first()
    user_now.like.append(post_now)
    like_user = post_now.like + 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('reels'))


@app.route('/dislikee/<int:id>')
def dislikee(id):
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == session['username']).first()
    user_now.like.remove(post_now)
    like_user = post_now.like - 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('reels'))


@app.route('/add_likeee/<int:id>')
def add_likeee(id):
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == session['username']).first()
    user_now.like.append(post_now)
    like_user = post_now.like + 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('top'))


@app.route('/dislikeee/<int:id>')
def dislikeee(id):
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == session['username']).first()
    user_now.like.remove(post_now)
    like_user = post_now.like - 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('top'))


@app.route('/add_likeeee/<int:id>')
def add_likeeee(id):
    user = current_user()
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == user.username).first()
    user_now.like.append(post_now)
    like_user = post_now.like + 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('username', username=user.username))


@app.route('/dislikeeee/<int:id>')
def dislikeeee(id):
    user = current_user()
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now = Users.query.filter(Users.username == user.username).first()
    user_now.like.remove(post_now)
    like_user = post_now.like - 1
    Reels.query.filter(Reels.id == id).update({
        'like': like_user
    })
    db.session.commit()
    return redirect(url_for('username', username=user.username))


@app.route('/unsave/<int:id>')
def unsave(id):
    user_now = Users.query.filter(Users.username == session['username']).first()
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now.reels.remove(post_now)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/savee<int:id>')
def savee(id):
    user = current_user()
    user_filter = Users.query.filter(Users.id == user.id).first()
    reel_filter = Reels.query.filter(Reels.id == id).first()
    user_filter.reels.append(reel_filter)
    db.session.commit()
    return redirect(url_for('username', username=user.username))


@app.route('/unsavee/<int:id>')
def unsavee(id):
    user = current_user()
    user_now = Users.query.filter(Users.username == session['username']).first()
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now.reels.remove(post_now)
    db.session.commit()
    return redirect(url_for('username', username=user.username))


@app.route('/delete/<int:reel>')
def delete(reel):
    user = current_user()
    filter = Reels.query.filter(Reels.id == reel).first()
    db.session.delete(filter)
    db.session.commit()
    return redirect(url_for('username', username=user.username))


@app.route('/deletee/<int:coom>/<int:reel>')
def deletee(coom, reel):
    user = current_user()
    filter = Comment.query.filter(Comment.id == coom).delete()
    db.session.commit()
    filter2 = Reels.query.filter(Reels.id == reel).first()
    soni = filter2.length_comment
    Reels.query.filter(Reels.id == reel).update({
        'length_comment': soni - 1
    })
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/saveee<int:id>')
def saveee(id):
    user = current_user()
    user_filter = Users.query.filter(Users.id == user.id).first()
    reel_filter = Reels.query.filter(Reels.id == id).first()
    user_filter.reels.append(reel_filter)
    db.session.commit()
    return redirect(url_for('reels'))


@app.route('/unsaveee/<int:id>')
def unsaveee(id):
    user = current_user()
    user_now = Users.query.filter(Users.username == session['username']).first()
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now.reels.remove(post_now)
    db.session.commit()
    return redirect(url_for('reels'))


@app.route('/saveeee<int:id>')
def saveeee(id):
    user = current_user()
    user_filter = Users.query.filter(Users.id == user.id).first()
    reel_filter = Reels.query.filter(Reels.id == id).first()
    user_filter.reels.append(reel_filter)
    db.session.commit()
    return redirect(url_for('top'))


@app.route('/unsaveeee/<int:id>')
def unsaveeee(id):
    user = current_user()
    user_now = Users.query.filter(Users.username == session['username']).first()
    post_now = Reels.query.filter(Reels.id == id).first()
    user_now.reels.remove(post_now)
    db.session.commit()
    return redirect(url_for('top'))


@app.route('/top')
def top():
    user = current_user()
    reels = Reels.query.order_by(Reels.id.desc()).all()
    return render_template('top.html', user=user, reels=reels)


@app.route('/profile')
def profile():
    return render_template('profile_users.html')


@app.route('/edit', methods=["POST", "GET"])
def edit():
    user = current_user()
    if request.method == "POST":
        gmail = request.form.get('gmail')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        bio = request.form.get('bio')
        photo = request.files['photo']
        folder = users_folder()
        hashed = generate_password_hash(password=password, method='sha256')
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            Users.query.filter(Users.id == user.id).update({
                "gmail": gmail,
                "name": name,
                "username": username,
                "password": hashed,
                "photo": photo_url,
                "bio": bio
            })
            db.session.commit()
            return redirect(url_for('edit', user=user))
        else:
            Users.query.filter(Users.id == user.id).update({
                "gmail": gmail,
                "name": name,
                "username": username,
                "password": hashed,
                "bio": bio
            })
            db.session.commit()
            return redirect(url_for('edit', user=user))
    return render_template('edit.html', user=user)


@app.route('/reels_add', methods=["POST", "GET"])
def reels_add():
    user = current_user()
    if request.method == "POST":
        video = request.files['video']
        folder = users_folder()
        location = request.form.get('location')
        caption = request.form.get('caption')
        if video and checkFile(video.filename):
            photo_file = secure_filename(video.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            video.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            add = Reels(user=user.id, sound="Orginal Sound", reel=photo_url,
                        reel_name=user.username, caption=caption, location=location, photo=user.photo, like=0,
                        length_comment=0)
            db.session.add(add)
            db.session.commit()
            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/<string:username>/#', methods=["POST", "GET"])
def followe(username):
    user = current_user()
    filter = Users.query.filter(Users.username == username).first()
    add = Follow(following_id=user.id, follower_id=filter.id)
    db.session.add(add)
    db.session.commit()
    user = current_user()
    reels = Reels.query.all()
    follow = Follow.query.filter(Follow.following_id == user.id).all()
    users = Users.query.all()
    return redirect(url_for('index'))


@app.route('/search', methods=["POST", "GET"])
def search():
    user = current_user()
    if request.method == "POST":
        search = request.form.get('search')
        filter = Users.query.filter(Users.username == search).first()
        return render_template('search.html', filter=filter, user=user)
    return render_template('search.html', user=user)


@app.route('/reels')
def reels():
    user = current_user()
    reels = Reels.query.order_by(Reels.id.desc()).all()
    return render_template('reels.html', user=user, reels=reels)


@app.route('/save<int:id>')
def save(id):
    user = current_user()
    user_filter = Users.query.filter(Users.id == user.id).first()
    reel_filter = Reels.query.filter(Reels.id == id).first()
    user_filter.reels.append(reel_filter)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/<string:username>')
def username(username):
    user = current_user()
    filter = Users.query.filter(Users.username == username).first()
    save = filter.reels
    print(save)
    reels = Reels.query.filter(Reels.user == filter.id).all()
    reel_count = Reels.query.filter(Reels.user == filter.id).count()
    follow = Follow.query.filter(Follow.follower_id == filter.id).count()
    curent = Follow.query.filter(Follow.follower_id == filter.id, Follow.following_id == user.id).first()
    return render_template('profile_users.html', username=username, filter=filter, reels=reels, follow=follow,
                           reel_count=reel_count, user=user, curent=curent, save=save)


@app.route('/<string:username>?', methods=["POST", "GET"])
def follow(username):
    user = current_user()
    if request.method == "POST":
        filter = Users.query.filter(Users.username == username).first()
        add = Follow(following_id=user.id, follower_id=filter.id)
        db.session.add(add)
        db.session.commit()
        reels = filter.reels
        reel_count = Reels.query.filter(Reels.user == filter.id).count()
        follow = Follow.query.filter(Follow.follower_id == filter.id).count()
        curent = Follow.query.filter(Follow.follower_id == filter.id, Follow.following_id == user.id).first()
        return render_template('profile_users.html', username=username, filter=filter, reels=reels, follow=follow,
                               reel_count=reel_count, user=user, curent=curent)
    return redirect(url_for('follow'))


@app.route('/<string:username>', methods=["POST", "GET"])
def unfollow(username):
    user = current_user()
    if request.method == "POST":
        filter = Users.query.filter(Users.username == username).first()
        Follow.query.filter(Follow.follower_id == filter.id, Follow.following_id == user.id).delete()
        db.session.commit()
        curent = Follow.query.filter(Follow.follower_id == filter.id, Follow.following_id == user.id).first()
        reels = filter.reels
        reel_count = Reels.query.filter(Reels.user == filter.id).count()
        follow = Follow.query.filter(Follow.follower_id == filter.id).count()
        return render_template('profile_users.html', username=username, filter=filter, reels=reels, follow=follow,
                               reel_count=reel_count, user=user, curent=curent)
    return redirect(url_for('unfollow'))


@app.route('/logout')
def logout():
    user = current_user()
    session['username'] = ""
    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run()
