from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/next")
def next():
    return render_template('person.html')

@app.route("/error")
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)