# Weatherly

#### Video Demo: [https://youtu.be/ArTsj71Rks0]

#### Description:
Weatherly is a weather application that provides users with the ability to authenticate, search for weather information, and manage their favorite cities.

## Features

### Authentication
- Users can register by providing a unique username and password.
- Existing users can log in with their username and password.

### Home
- Users can search for weather information by city name or coordinates.
- The search results display detailed weather information.
- Users can also view the weather information of their favorite cities.

### Weather Search by City 
- Users can search for weather information by city name.
- The search results display detailed weather information for that city.

### Weather Search by Coordinates 
- Users can search for weather information by coordinates.
- The search results display detailed weather information for those coordinates.

### Favorites
- Users can view weather information for their favorite cities.
- Favorites can be added, viewed, and managed through dedicated pages.

### Add Favorites
- Users can add cities to their favorites by typing the city name and clicking "Add to Favorites."

### Manage Favorites
- Users can view a table of their favorite cities with a delete option to remove unwanted entries.

### Log Out
- Users can log out to secure their account.

## Getting Started

1. Clone the repository.
2. Install the necessary dependencies.
3. Set up a database for user information and favorites.
4. Run the application.

## Usage

1. Access the homepage and either log in or register.
2. Explore the weather information by searching for cities or coordinates.
3. Manage favorite cities through the "Favorites" and "Manage Favorites" pages.
4. Log out when finished.

## Technologies Used
- **Frontend:**
  - HTML
  - CSS
  - Bootstrap library
  - JavaScript
  - jQuery

- **Backend:**
  - Flask (Python web framework)
  - SQL (for database)
  - [cs50 library](https://github.com/cs50/python-cs50) (used for database interactions)
  - [Flask-Session](https://pythonhosted.org/Flask-Session/) (for session management)
  - [Werkzeug](https://palletsprojects.com/p/werkzeug/) (for hashing passwords)

- **API:**
  - [OpenWeatherMap](https://openweathermap.org/) (used for weather data)

- **Other:**
  - os (Python built-in module)
  - [requests library](https://docs.python-requests.org/en/latest/) (used for making HTTP requests)
  - [functools module](https://docs.python.org/3/library/functools.html) (used for functional programming)

## License
This project is licensed under the [MIT License](LICENSE).


>>>>>>> 1329b53 (Pushing weatherly files to git)
