from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from werkzeug.urls import url_parse

from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import EditProfileForm, EmptyForm, LoginForm, PostForm, RegistrationForm
from app.models import Post, User


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live.')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    new = url_for('index', page=posts.prev_num) if posts.has_prev else None
    old = url_for('index', page=posts.next_num) if posts.has_next else None

    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, new=new, old=old)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    new = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    old = url_for('explore', page=posts.next_num) if posts.has_next else None

    return render_template('index.html', title='Explore', posts=posts.items,
                           new=new, old=old)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
            next = url_for('index')
        return redirect(next)

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user.')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()

    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    new = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    old = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None

    return render_template('user.html', user=user, posts=posts,
                           form=form, new=new, old=old)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Updation fulfilled')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', title='Edit profile', form=form)


@app.route('/follow/<username>', methods=('POST',))
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself.')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You followed {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=('POST',))
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself.')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You unfollowed {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
