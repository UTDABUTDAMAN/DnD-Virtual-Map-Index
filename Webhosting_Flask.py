

from flask import Flask


app = Flask(_name_)

    # a simple page that says hello
@app.route('/')
    def hello():
        return 'Hello, World!'

