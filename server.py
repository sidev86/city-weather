from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

def translate_weather_state(weather_data):
    weather = weather_data["weather"][0]["description"].lower()
    if weather == "few clouds":
        status  = "poco nuvoloso"
    elif weather == "scattered clouds":
        status = "nuvole sparse"
    elif weather == "broken clouds":
        status = "parz. nuvoloso"
    elif weather == "overcast clouds":
        status = "nuvoloso"
    elif weather == "shower rain":
        status = "pioggia a rovesci"
    elif weather == "moderate rain":
        status = "pioggia moderata"
    elif weather == "light rain":
        status = "lieve pioggia"
    elif weather == "thunderstorm":
        status = "temporale"
    elif weather == "snow":
        status = "neve"
    elif weather == "mist":
        status = "nebbia"
    elif weather == "clear sky":
        status = "soleggiato"
    elif weather == "rain":
        status = "pioggia"
    else:
        status = weather
    return status.capitalize();

app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not bool(city.strip()):
        city = "Milan"
    weather_data = get_current_weather(city)
    if not weather_data["cod"] == 200:
        return render_template('city-not-found.html')
    weather = translate_weather_state(weather_data)
    return render_template('weather.html', title=weather_data["name"], status = weather, temp=f"{weather_data["main"]["temp"]:.1f}", feels_like=f"{weather_data["main"]["feels_like"]:.1f}")
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)