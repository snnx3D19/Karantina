from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session
from data.users import User
from data.entertainment import Entertainment
from data.new_ent import New_EntForm
from data.register import RegisterForm
from data.login_form import LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# +
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

# +
@app.route('/films')
def films_link():
    return redirect("http://z2.lordfilms.host/")

# +
@app.route('/news_link')
def news_link():
    return redirect("https://yandex.ru/news/rubric/world")

# +
@app.route('/new_kino')
def new_kino():
    session = db_session.create_session()
    ents = session.query(Entertainment).filter(Entertainment.ent_type == "kino")
    users = session.query(User).all()
    names = {name.id: (name.nickname) for name in users}
    return render_template("index.html", ents=ents, names=names, title='Кино')

# +
@app.route('/new_music')
def new_music():
    session = db_session.create_session()
    ents = session.query(Entertainment).filter(Entertainment.ent_type == "music")
    users = session.query(User).all()
    names = {name.id: (name.nickname) for name in users}
    return render_template("index.html", ents=ents, names=names, title='Музыка')

# +
@app.route('/new_games')
def new_games():
    session = db_session.create_session()
    ents = session.query(Entertainment).filter(Entertainment.ent_type == "game")
    users = session.query(User).all()
    names = {name.id: (name.nickname) for name in users}
    return render_template("index.html", ents=ents, names=names, title='Игры')

# +
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

# +
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

# -
@app.route("/")
def index():
    session = db_session.create_session()
    ents = session.query(Entertainment).all()
    users = session.query(User).all()
    names = {name.id: (name.nickname) for name in users}
    return render_template("index.html", ents=ents, names=names, title='Главная страница')

# +
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

# +
@app.route('/newent', methods=['GET', 'POST'])
def new_ent():
    new_form = New_EntForm()
    if new_form.validate_on_submit():
        session = db_session.create_session()
        ents = Entertainment(
            ent=new_form.ent.data,
            ent_type=new_form.ent_type.data,
            content=new_form.content.data
        )
        session.add(ents)
        session.commit()
        return redirect('/')
    return render_template('new_ents.html', title='Добавление развлечения', form=new_form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/users.sqlite")
    app.run()
    

if __name__ == '__main__':
    main()
