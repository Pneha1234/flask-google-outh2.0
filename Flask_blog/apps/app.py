from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from auth import OAuthSignIn

from models.users import User

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'this is very secret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.find_by_id(id)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    print('---------------', current_user)
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()

    if email is None:
        print('Authentication failed.')
        return redirect(url_for('index'))

    user = User.find_or_create_by_email(email)
    login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
