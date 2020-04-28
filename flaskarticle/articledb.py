"""
连接数据库:
"""
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


"""
1.当使用 SQLite 数据库（包括其他多数数据库的 Python 库）时，
第一件事就是创建 一个数据库的连接。所有查询和操作都要通过该连接来执行，
完事后该连接关闭。在网络应用中连接往往与请求绑定。
在处理请求的某个时刻，连接被创建。在发送响应 之前连接被关闭。

"""
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('article.sql') as f:
        db.executescript(f.read().decode('utf8'))



"""
2.在 db.py 文件中添加 Python 函数，用于运行以上 SQL 命令：
"""
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

"""
3.在应用中注册:

close_db 和 init_db_command 函数需要在应用实例中注册，否则无法使用。 
然而，既然我们使用了工厂函数，那么在写函数的时候应用实例还无法使用。
代替地， 我们写一个函数，把应用作为参数，在函数中进行注册。

"""

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)