from flask import Flask
from app import app


@app.route("/")
def index():
    return "Hello,World!"


# @app.route("/<name>")
# def print_name(name):
#     return f"Hello, {name}"


if __name__ == "__main__":
    app.run(debug=True)
