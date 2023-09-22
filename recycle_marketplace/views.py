from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from recycle_marketplace import app, db
from recycle_marketplace.forms import LoginForm, RegistrationForm, ItemForm, ReviewForm
from recycle_marketplace.models import User, Item, Review

@app.route('/')
@app.route('/index')
@login_required
def index():
    items = Item.query.all()
    return render_template('index.html', title='Home', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/list_item', methods=['GET', 'POST'])
@login_required
def list_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(title=form.title.data, description=form.description.data, price=form.price.data, owner=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item is now live!')
        return redirect(url_for('index'))
    return render_template('list_item.html', title='List Item', form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if 'q' in request.args:
        q = request.args.get('q')
        items = Item.query.filter(Item.title.contains(q)).all()
        return render_template('search.html', title='Search', items=items)
    return render_template('search.html', title='Search')

@app.route('/item/<id>', methods=['GET', 'POST'])
@login_required
def item(id):
    item = Item.query.get(id)
    if item is None:
        flash('Item not found.')
        return redirect(url_for('index'))
    return render_template('item.html', title='Item', item=item)

@app.route('/write_review/<username>', methods=['GET', 'POST'])
@login_required
def write_review(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found.')
        return redirect(url_for('index'))
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(content=form.content.data, rating=form.rating.data, reviewer=current_user, reviewed=user)
        db.session.add(review)
        db.session.commit()
        flash('Your review is now live!')
        return redirect(url_for('index'))
    return render_template('write_review.html', title='Write Review', form=form)
