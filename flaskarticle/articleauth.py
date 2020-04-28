import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.articledb import get_db

"""
创建蓝图:

Blueprint 是一种组织一组相关视图及其他代码的方式。
与把视图及其他代码直接注册到应用的方式不同，蓝图方式是把它们注册到蓝图，
然后在工厂函数中 把蓝图注册到应用。
1.Flaskr 有两个蓝图，一个用于认证功能，另一个用于博客帖子管理。
每个蓝图的代码都在一个单独的模块中。使用博客首先需要认证，因此我们先写认证蓝图。
"""


bp = Blueprint('articleauth', __name__, url_prefix='/articleauth')


"""
第一个视图：注册

当用访问 /auth/register URL 时， register 视图会返回用于填写注册 内容的表单的 HTML 。当用户提交表单时，视图会验证表单内容，然后要么再次 显示表单并显示一个出错信息，要么创建新用户并显示登录页面。

这里是视图代码，下一页会写生成 HTML 表单的模板。

"""


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT masterid FROM tb_master WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO tb_master (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('articleauth.login'))

        flash(error)

    return render_template('articleauth/register.html')


"""
登录:这个视图和上述 register 视图原理相同。

"""


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM tb_master WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            for i in user:
                print(i)
            print("111111",user['masterid'])
            session['user_id'] = user['masterid']

            return redirect(url_for('articleblog.index'))

        flash(error)

    return render_template('articleauth/login.html')


"""
现在用户的 id 已被储存在 session 中，可以被后续的请求使用。 
请每个请求的开头，如果用户已登录，那么其用户信息应当被载入，以使其可用于其他视图。
"""


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM tb_master WHERE masterid = ?', (user_id,)
        ).fetchone()


"""
注销:注销的时候需要把用户 id 从 session 中移除。 
然后load_logged_in_user就不会在后继请求中载入用户了。

"""


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('articleblog.index'))


"""
在其他视图中验证:用户登录以后才能创建、编辑和删除博客帖子。
在每个视图中可以使用 装饰器 来完成这个工作。

"""


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('articleauth.login'))

        return view(**kwargs)

    return wrapped_view

