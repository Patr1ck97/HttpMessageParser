from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def test():
    print(request.method)
    print(request.form)
    print(request.json)
    print(request.headers)
    return "111"


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
