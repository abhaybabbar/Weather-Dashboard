from django.shortcuts import render
from django.http import HttpResponse
from .forms import CityForm
import requests
from .models import City
from django.conf import settings
# Create your views here.

def get_weather_data(city_name):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
    'q': city_name,
    'appid': settings.OWM_API_KEY,
    'units': 'metric',
    }
    response = requests.get(url, params=params)

    if response.status_code>=400:
        weather_data = None
    
    else:
        json_response = response.json()
        weather_data = {
        'temp': json_response['main']['temp'],
        'min_temp': json_response['main']['temp_min'],
        'max_temp': json_response['main']['temp_max'],
        'city_name': json_response['name'],
        'country_name': json_response['sys']['country'],
        'lat': json_response['coord']['lat'],
        'lon': json_response['coord']['lon'],
        'weather': json_response['weather'][0]['main'],
        'weather_desc': json_response['weather'][0]['description'],
        'humidity': json_response['main']['humidity'],
        'pressure': json_response['main']['pressure'],
        'wind_speed': json_response['wind']['speed'],
        }
    return weather_data

def home(request):
    form = CityForm()
    if request.method=="POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            city_name = form.cleaned_data.get('city_name')
            weather_data = get_weather_data(city_name)
            
    elif request.method=="GET":
        try:
            city_name = City.objects.latest('date_added').city_name
        except:
            city_name = "Delhi"
        weather_data = get_weather_data(city_name)
    context = {'form': form, 'weather_data': weather_data}
    return render(request, 'home.html', context=context)

def history(request):
    cities = City.objects.all().order_by('-date_added')[:5]
    weather_data_list = []
    for city in cities:
        weather_data_list.append(get_weather_data(city.city_name))
    
    context = {'weather_data_list': weather_data_list}
    return render(request, 'history.html', context=context)