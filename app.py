# Importing function and dict from api.py
from api import get_weather, get_favt_weather

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
# Flask component providing lib for hashing passwords
from werkzeug.security import check_password_hash, generate_password_hash

# Configure the app
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

api_key = "dee1639976652cfd11372537874e3826"

db = SQL("sqlite:///weather.db")

# Create a dict with all the weather information above for better design and pass it to render_template

# Create the database
db.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
"""
)

# Creating favorite_cities table to be used in index to add cities
db.execute("""
    CREATE TABLE IF NOT EXISTS favorite_cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        city_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")


@app.route('/register', methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # When user is submitting (POST)
    if request.method == "POST":
        username = request.form.get("username") # Links to the name attribute in html   
        password = request.form.get("password")   
        confirm_password = request.form.get("confirm_password")   
        # Validations and checks
        if not username:
            return jsonify({"error": "Please enter username"}), 400
        elif not password:
            return jsonify({"error": "Must provide password"}), 400
        elif not confirm_password:
            return jsonify({"error": "Please enter matching confirmation password"}), 400
        elif (password != confirm_password):
            return jsonify({"error": "Passwords do not match, try again!"}), 400
        # Ensure username is not already taken
        existing_username = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_username:
            return jsonify({"error": "username already exists"}), 400

        # If all good, proceed with the registeration
        else:
            # Add to db
            db.execute("""
                       INSERT INTO users (username, hash) VALUES (?, ?)""", 
                       username, generate_password_hash(password),
                       )
            # Retrieve the userid after inserting into the database
            user_id = db.execute("SELECT id FROM users WHERE username = ?", username)

            # Once registeration is done, keep track of the user
            session["user_id"] = user_id[0]["id"]

            # Redirect user to home page (index)
            return redirect("/")

    # For get request
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return jsonify({"error": "must provide username"}), 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            return jsonify({"error": "must provide password"}), 403

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        print(f"rows type: {type(rows)}")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return jsonify({"error": "invalid username and/or password"}), 403

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route('/')
@login_required
def index():
    user_id = session["user_id"]

    # Fetch user's favorite cities from db
    cities = db.execute("SELECT city_name FROM favorite_cities WHERE user_id = ?", user_id)
    # Call the get_favt_weather function to get weather information
    weather_info_list = get_favt_weather(cities)

    # Zipping the data for iteration in the template
    zipped_data = zip(cities, weather_info_list)

    return render_template('index.html', zipped_data=zipped_data)


@app.route('/add_favorites', methods=["GET", "POST"])
@login_required
def add_favorites():
    if request.method == "POST":
        user_id = session["user_id"]
        city_name = request.form.get("city_name").title()

        # Validate and insert in db
        if city_name:
            db.execute("INSERT INTO favorite_cities (user_id, city_name) VALUES (?,?)", user_id, city_name)

        return redirect("/")

    else:
        return render_template("add_favorites.html")


# This function will only show the favorite_cities
@app.route('/favorites')
@login_required
def favorites():
    # Fetch user's favorite cities from the database
    user_id = session["user_id"]
    favorite_cities = db.execute("SELECT city_name FROM favorite_cities WHERE user_id = ?", user_id)

    # Call the get_favt_weather function to get weather information
    weather_info = get_favt_weather(favorite_cities)
    # Zipping the data for iteration in the template

    zipped_data = zip(favorite_cities, weather_info)

    return render_template('favorites.html', zipped_data = zipped_data)


# This function is used to delete and manage favorites
@app.route('/manage_favorites', methods=['GET', 'POST'])
@login_required
def manage_favorites():
    if request.method == 'GET':
        # Retrieve the user's favorite cities from the database with a delete button
        user_id = session['user_id']
        favorites = db.execute('SELECT * FROM favorite_cities WHERE user_id = ?', user_id)

        return render_template('manage_favorites.html', favorites=favorites)

    # To delete a favorite city
    elif request.method == 'POST':
        # Retrieve the city_id from the form
        city_id = request.form.get('city_id')

        # Delete the favorite city from the database
        db.execute('DELETE FROM favorite_cities WHERE id = ?', city_id)

        # Redirect to the manage favorites page after deleting
        return redirect('/manage_favorites')


@app.route('/weather', methods=['GET'])
@login_required
def weather():
    return get_weather()

@app.route('/favt_weather', methods=['GET'])
@login_required
def favt_city_weather():
    # Fetch user's favorite cities from the database
    user_id = session["user_id"]
    cities = db.execute("SELECT city_name FROM favorite_cities WHERE user_id = ?", user_id)
    print("Cities:", cities)  # Add this line for debugging
    weather_info_list = get_favt_weather(cities)


    return jsonify({'weather_info_list': weather_info_list})


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Starting a development server when script is run directly and not imported as module
if __name__ == '__main__':
    app.run(debug=True)
