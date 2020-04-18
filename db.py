from mongoengine.connection import connect

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = connect(host=current_app.config['DB_MONGOOSE'])
    return g.db


def get_connection():
    connection = connect(
        host=current_app.config['DB_MONGOOSE'])
    print(f"connected to {connection}")
