import datetime
from random import choice

from flask import Flask, render_template, request, redirect
from sqlalchemy import desc

from db.database import init_db, db_session
from models.histories import Histories
from models.restaurants import Restaurants

app = Flask(__name__)


@app.before_first_request
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def start():
    now = datetime.datetime.now()
    return render_template('start.html', nav='start', now=now)


@app.route("/draw")
def draw():
    restaurants = Restaurants.query.all()
    if not restaurants:
        return redirect("/create-restaurant")

    try:
        random_restaurant = choice(restaurants)
        restaurant = Restaurants.query.get(random_restaurant.id)
        restaurant.draw += 1
        history = Histories(restaurant_id=restaurant.id)

        db_session.add(history)
        db_session.commit()
    except:
        db_session.rollback()
        return redirect("/")

    now = datetime.datetime.now()

    return render_template('draw.html', restaurant=restaurant, now=now)


@app.route("/create-restaurant", methods=["GET", "POST"])
def create_restaurant():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        site_url = request.form.get('site_url')

        restaurant = Restaurants(name, description, site_url)
        db_session.add(restaurant)
        db_session.commit()

        return redirect("/restaurants")
    return render_template('create-restaurant.html')


@app.route("/restaurants")
def restaurant_list():
    restaurants = Restaurants.query.all()
    return render_template('restaurant.html', nav='restaurants', restaurants=restaurants)


@app.route("/delete-restaurant")
def delete_restaurant():
    id = request.args.get('id')
    restaurant = Restaurants.query.filter(Restaurants.id == id).first()

    if restaurant:
        db_session.delete(restaurant)
        db_session.commit()
    return redirect("/restaurants")


@app.route("/edit-restaurant", methods=["GET", "POST"])
def edit_restaurant():
    id = request.args.get('id')
    restaurant = Restaurants.query.filter(Restaurants.id == id).first()

    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        site_url = request.form.get('site_url')

        restaurant.name = name
        restaurant.description = description
        restaurant.site_url = site_url
        restaurant.modified_time = datetime.datetime.now()

        db_session.commit()
        return redirect("/restaurants")
    return render_template("edit-restaurant.html", restaurant=restaurant)


@app.route("/history")
def history():
    histories = Histories.query.order_by(desc(Histories.created_time)).limit(20)
    return render_template('history.html', nav='history', histories=histories)


@app.route("/top")
def top():
    restaurants = Restaurants.query.order_by(desc('draw')).limit(5)

    return render_template('top.html',nav='top', restaurants=restaurants)


def date_time_format(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


def meal_format(value):
    if value.hour in range(4, 10):
        return "Breakfast"
    elif value.hour in range(10, 16):
        return "Lunch"
    elif value.hour in range(16, 22):
        return "Dinner"
    return "Supper"


app.jinja_env.filters['meal'] = meal_format
app.jinja_env.filters['datetime'] = date_time_format
app.jinja_env.auto_reload = True
app.run(debug=True)
