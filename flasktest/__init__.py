"""
一、应用工厂:
创建 flaskr文件夹并且文件夹内添加 __init__.py 文件。
__init__.py 有两个作用：一是包含应用工厂；
二是告诉Python flaskr文件夹应当视作为一个包。

"""

import os

from flask import Flask


def create_app(test_config=None):
    """
    创建一个工厂函数：模块化管理（配置、导入注册等）
    :param test_config:
    :return:
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flasktest.sqlite'),
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
        return 'Hello, World! my flasktest '

    # 导入数据初始化命令
    from . import db

    db.init_app(app)

    # 导入注册认证蓝图：auth.bp
    from . import auth
    app.register_blueprint(auth.bp)

    # 导入注册博客蓝图(主页)：blog.bp

    from . import blog
    app.register_blueprint(blog.bp)


    # 导入markdown蓝图：mark.bp
    from . import mark
    app.register_blueprint(mark.bp)

    # 导入imag蓝图：imag.bp
    from . import imag
    app.register_blueprint(imag.bp)

    #app.add_url_rule('/', endpoint='index')


    return app

