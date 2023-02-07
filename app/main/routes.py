from datetime import datetime

from flask import (
    current_app,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)

from flask_babel import _, get_locale
from flask_login import current_user, login_required
from langdetect import LangDetectException, detect

from app import db
from app.main import blueprint
from app.main.forms import EditProfileForm, EmptyForm, PostForm
from app.models import Post, User
from app.translate import translate


@blueprint.route('/', methods=('GET', 'POST'))
@blueprint.route('/index', methods=('GET', 'POST'))
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''

        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live.'))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    new = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    old = url_for('main.index', page=posts.next_num) if posts.has_next else None

    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, new=new, old=old)


@blueprint.route('/delete/<int:id>')
@login_required
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    flash(_('Post deleted.'))
    return redirect(url_for('main.index'))


@blueprint.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    new = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
    old = url_for('main.explore', page=posts.next_num) if posts.has_next else None

    return render_template('index.html', title=_('Explore'), posts=posts.items,
                           new=new, old=old)


@blueprint.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()

    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    new = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    old = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None

    return render_template('user.html', user=user, posts=posts,
                           form=form, new=new, old=old)


@blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())


@blueprint.route('/edit_profile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash(_('Changes saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', title=_('Edit profile'), form=form)


@blueprint.route('/follow/<username>', methods=('POST',))
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself.'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You followed %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@blueprint.route('/unfollow/<username>', methods=('POST',))
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself.'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You unfollowed %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@blueprint.route('/translate', methods=('POST',))
@login_required
def translate_text():
    return jsonify({
        'text': translate(request.form['text'],
                          request.form['source_language'],
                          request.form['destination_language'])
    })
