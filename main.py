from flask import Flask, render_template, request, jsonify, make_response, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://appCarFuel:X690!6GM2fK6iF8lH6@dbhost:3306/carFuel")

Base = declarative_base()

app = Flask(__name__)

SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config['SECRET_KEY'] = 'AJDJRJS24$($(#$$33--'

"""
User*: appCarFuel
Password*: X690!6GM2fK6iF8lH6
Host: dbhost (Mariadb Container Name)
Port: 3306
Database: carFuel
"""

db = SQLAlchemy(app)

base_url = "http://127.0.0.1:5000"


class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))


class Car(Base):
    __tablename__ = 'car'

    car_number = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100))
    gasoline_type = db.Column(db.String(100))


class Transaction(Base):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    car = db.Column(db.Integer, db.ForeignKey('car.car_number'))
    current_mileage = db.Column(db.String(100))
    daily_mileage = db.Column(db.String(100))
    date = db.Column(db.Date)
    liter = db.Column(db.Integer)
    price = db.Column(db.Integer)


Base.metadata.create_all(engine)

"""
    Apis
"""


@app.route('/create-user/', methods=['POST'])
def user():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            # Create a session
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=engine)
            session = Session()

            data = User(username=username, email=email, password=password)
            session.add(data)
            session.commit()

            session.close()
            return make_response({"key": "Added Successfully"}, 200)
        except Exception as e:
            print(str(e))
            return make_response({"key": "username already exists"}, 400)


@app.route('/signup/')
def signup():
    return render_template("signup.html", base_url=base_url)


@app.route('/transactions/', methods=['GET', 'POST'])
def transactions():
    if 'user' in session:
        if request.method == "POST":
            user_id = session["user"]
            car_num_id = request.form['car_num_id']
            current_mileage = request.form['current_mileage']
            daily_mileage = request.form['daily_mileage']
            date = request.form['date']
            liter = request.form['liter']
            price = request.form['price']

            print(user_id, car_num_id, current_mileage, daily_mileage, date, liter, price)

            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=engine)
            dbsession = Session()

            data = Transaction(
                user=user_id,
                car=car_num_id,
                current_mileage=current_mileage,
                daily_mileage=daily_mileage,
                date=date,
                liter=liter,
                price=price
            )
            dbsession.add(data)
            dbsession.commit()

            dbsession.close()
            return make_response({"key": "Added Successfully"}, 200)

        else:
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=engine)
            dbsession = Session()

            cars = dbsession.query(Car).all()
            dbsession.close()
            return render_template("transactions.html", base_url=base_url, cars=cars)
    else:
        return redirect("/login/")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Create a session
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine)
        dbsession = Session()

        user = dbsession.query(User).filter_by(username=username, password=password)
        dbsession.close()
        if user:
            session["user"] = user[0].id
            return make_response({"key": "Login success"}, 200)
        else:
            return make_response({"key": "Wrong Email or Password"}, 400)
    else:
        if 'user' in session:
            return redirect('/')
        else:
            return render_template("login.html", base_url=base_url)


@app.route('/')
def index():
    if 'user' in session:
        user = session['user']
        print(user)
        return render_template("dashboard.html", base_url=base_url)
    else:
        return redirect("/login/")


@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/get_my_transactions/')
def get_transactions():
    if 'user' in session:
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine)
        dbsession = Session()

        my_transactions = dbsession.query(Transaction).filter_by(user=session['user'])
        dbsession.close()
        list = []
        for d in my_transactions:
            obj = {
                'user': d.user,
                'car': d.car,
                'current_mileage': d.current_mileage,
                'daily_mileage': d.daily_mileage,
                'date': d.date,
                'liter': d.liter,
                'price': d.price
            }
            list.append(obj)
        return make_response(jsonify(transactions=list), 200)
    else:
        return redirect("/login/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
