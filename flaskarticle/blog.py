"""
博客蓝图:

博客蓝图与验证蓝图所使用的技术一样。博客页面应当列出所有的帖子，允许已登录 用户创建帖子，并允许帖子作者修改和删除帖子。

当你完成每个视图时，请保持开发服务器运行。当你保存修改后，请尝试在浏览器中 访问 URL ，并进行测试。

蓝图

定义蓝图并注册到应用工厂。

"""


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskarticle.auth import login_required
from flaskarticle.db import get_db


bp = Blueprint('blog', __name__)


"""
索引:
索引会显示所有帖子，最新的会排在最前面。为了在结果中包含 user 表中的 作者信息，使用了一个 JOIN 。

"""


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


"""
创建:
create 视图与 register 视图原理相同。要么显示表单，要么发送内容 已通过验证且内容已加入数据库，或者显示一个出错信息。

先前写的 login_required 装饰器用在了博客视图中，这样用户必须登录以后 才能访问这些视图，否则会被重定向到登录页面。

"""


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


"""
更新:
update 和 delete 视图都需要通过 id 来获取一个 post ，并且 检查作者与登录用户是否一致。为避免重复代码，可以写一个函数来获取 post ， 并在每个视图中调用它。

"""


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['user_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


"""
删除:
删除视图没有自己的模板。删除按钮已包含于 update.html 之中，该按钮指向 /<id>/delete URL 。既然没有模板，该视图只处理 POST 方法并重定向到 index 视图。

"""


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

