from flask import Flask

app = Flask(__name__)

from appmain.routes import main
app.register_blueprint(main)
