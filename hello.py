"""
一个最简单的 Flask 应用可以是单个文件
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)