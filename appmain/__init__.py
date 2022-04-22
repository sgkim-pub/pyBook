from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = 'e2a14e9612b8bdfc57201cfce12b6c8f'

from appmain.routes import main
app.register_blueprint(main)

from appmain.user.routes import user
app.register_blueprint(user)
