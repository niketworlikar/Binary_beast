import os
from flask import Flask,render_template, url_for,request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('dashboard.html')
APP_ROOT =os.path.dirname(os.path.abspath(__file__))
@app.route("/user.html")
def user():
    return render_template('user.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    target = os.path.join(APP_ROOT, 'pics')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    print(request)
    if request.method == 'POST':
      f = request.files['file']
      print(target)
      f.save(os.path.join(target,secure_filename(f.filename)))
      return 'file uploaded successfully'

    return render_template("complete.html")



if __name__ == "__main__":
    app.run()
