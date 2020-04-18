import os

from flask import Flask


def create_app():
    # Create and configure the app
    print(__name__)
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['DB_MONGOOSE'] = 'mongodb+srv://nelsonrds:connect98@cluster0-lq52p.mongodb.net/mongo-dev-db?retryWrites=true&w=majority'

    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import product
    app.register_blueprint(product.bp)
    app.add_url_rule('/', endpoint='index')

    from . import db

    with app.app_context():
        db.get_db()

    return app
