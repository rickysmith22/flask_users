from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'userdb.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), unique=False)
    lname = db.Column(db.String(50), unique=False)

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

class UserSchema(ma.Schema):
    class Meta:
        fields = ('fname', 'lname')

user_schema = UserSchema()
users_schema = UserSchema(many=True)



# @app.route("/")
# def home():
#     return render_template('index.html')

@app.route("/user", methods=["POST"])
def add_user():
    fname = request.json['fname']
    lname = request.json['lname']

    new_user = User(fname, lname)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)


@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)

@app.route("/", methods=["GET"])
def get_user():
    all_users = User.query.all()
    results = users_schema.dump(all_users)
    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)