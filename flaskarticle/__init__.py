"""
一、应用工厂:
创建 flaskarticle 文件夹并且文件夹内添加 __init__.py 文件。
__init__.py 有两个作用：一是包含应用工厂；
二是告诉Python flaskarticle文件夹应当视作为一个包。
"""

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskarticle.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 在工厂中导入并调用这个函数。在工厂函数中把新的代码放到函数的尾部，返回应用代码的前面。
    from . import articledb

    articledb.init_app(app)

    # 导入认证蓝图：articleauth.bp

    from . import articleauth
    app.register_blueprint(articleauth.bp)

    # 导入博客蓝图：

    from . import articleblog
    app.register_blueprint(articleblog.bp)
    #app.add_url_rule('/', endpoint='index')

    # 导入markdown蓝图
    from . import articlemark
    app.register_blueprint(articlemark.bp)
    app.add_url_rule('/', endpoint='index')


    return app

