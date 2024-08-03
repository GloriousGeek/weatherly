from flask import jsonify, request, render_template, session
import requests
from cs50 import SQL
from flask_session import Session

db = SQL("sqlite:///weather.db")


# # Defining a function to use it in other files as well.
# def get_weather_info:

# Defining a dynamic weather function
def get_weather():
    # Using try to avoid web app to crash due to api fetching difficulties
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        city_name = request.args.get('city_name')

        api_key = "dee1639976652cfd11372537874e3826"

        # Ensure api_key is provided
        if not api_key:
            return jsonify({'error': 'API key is missing'}), 400

        # Constructing api url
        if (lat is None or lon is None) and city_name is None:
            return jsonify({'error': 'Provide either lat and lon or city_name'}), 400
        
        # Server side to ensure if user enters both lat and lon
        if (lat is None and lon is not None) or (lon is None and lat is not None):
            return jsonify({'error': 'Please enter both Latitude and Longitude or leave both empty.'}), 400
        
        # If coordinates exist
        if lat and lon:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
            # api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
        
        elif city_name:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
            # api_url = f"https://api.openweathermap.org/data/3.0/weather?q={city_name}&appid={api_key}"

        else:
            return jsonify({'error': 'Invalid input'}), 400
        
        # Making API GET request
        response = requests.get(api_url)

        # Handling API response
        if response.status_code == 200:
            weather_data = response.json()
            # Print to see 
            print(weather_data)

            # Extract relevant weather information
            name = weather_data['name']
            temperature_kelvin = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            feels_like = weather_data['main']['feels_like']
            wind_speed = weather_data['wind']['speed']
            icon = weather_data['weather'][0]['icon']
            
            # Convert temperature from Kelvin to Celsius
            temperature_celsius = round(temperature_kelvin - 273.15, 2)

            feels_celsius = round(feels_like - 273.15, 2)

            # Create a dict with all the weather information above for better design and pass it to render_template
            weather_info = {
                "name": name,
                "temperature": temperature_celsius,
                "humidity": humidity,
                "feels_like": feels_celsius,
                "wind_speed": wind_speed,
                "icon": icon
            }

            return render_template('weather.html', weather_info = weather_info)

        else:
            # Print the response content for debugging
            print(response.content)
            print("Hello! Error fetching data")

            # If the API call fails, return an error message
            error_message = f"Error fetching weather data. Status code: {response.status_code}"
            return render_template('error.html', error_message=error_message)
    
    
    except (requests.RequestException, ValueError, KeyError, IndexError) as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error     
    
def get_favt_weather(cities):
    try:
        user_id = session["user_id"]

        # Fetch user's favorite cities from db
        cities = db.execute("SELECT city_name FROM favorite_cities WHERE user_id = ?", user_id)

        api_key = "dee1639976652cfd11372537874e3826"

        # Ensure api_key is provided
        if not api_key:
            return jsonify({'error': 'API key is missing'}), 400

        if cities:
            # Extracting city names from the list of dictionaries
            city_names = [city['city_name'] for city in cities]

            # Constructing the API URL for each city
            api_urls = [f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" for city in city_names]

            # Fetching weather information for each city
            weather_info_list = []
            for api_url in api_urls:
                response = requests.get(api_url)
                if response.status_code == 200:
                    weather_data = response.json()
                    # Extract relevant weather information
                    name = weather_data['name']
                    temperature_kelvin = weather_data['main']['temp']
                    humidity = weather_data['main']['humidity']
                    feels_like = weather_data['main']['feels_like']
                    wind_speed = weather_data['wind']['speed']
                    icon = weather_data['weather'][0]['icon']
                    # Convert temperature from Kelvin to Celsius
                    temperature_celsius = round(temperature_kelvin - 273.15, 2)
                    feels_celsius = round(feels_like - 273.15, 2)
                    # Create a dict with all the weather information for better design
                    weather_info = {
                        "name": name,
                        "temperature": temperature_celsius,
                        "humidity": humidity,
                        "feels_like": feels_celsius,
                        "wind_speed": wind_speed,
                        "icon": icon
                    }
                    # Append the weather information to the list
                    weather_info_list.append(weather_info)
                else:
                    # If the API call fails for a city, append an error message to the list
                    error_message = f"Error fetching weather data for {name}. Status code: {response.status_code}"

                    weather_info_list.append({'error': error_message})
            
            print("Weather Info List:", weather_info_list)  # Add this line for debugging


            # Pass the list of weather information to render_template
            # return render_template('favorites.html', weather_info_list=weather_info_list)
            return weather_info_list

        else:
            return jsonify({'error': 'No favorite cities found'}), 400

    except (requests.RequestException, ValueError, KeyError, IndexError) as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error
