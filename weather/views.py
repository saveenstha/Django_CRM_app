from django.shortcuts import render
from django.http import Http404
import requests
import json
import urllib.request
from urllib.error import HTTPError
from django.views.generic import ListView, DetailView
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            city = request.POST['city']
            res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid=3c9c768e17fe22f10bd1f3599c47fa87').read()
            json_data = json.loads(res)
            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon'])+' '+str(json_data['coord']['lat']),
                "temp": str(json_data['main']['temp'])+'k',
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
            }
        except HTTPError:
            error_message = "The entered city is not valid. Please enter valid city"
            return render(request, 'weather/home.html', {'error_message': error_message})


    else:
        city = ''
        data = {}
    return render(request, 'weather/home.html', {'data': data, 'city': city})


def CNJokes(request):

    categories = requests.get('https://api.chucknorris.io/jokes/categories').json()

    if request.method == "GET":
        url = 'https://api.chucknorris.io/jokes/random'

    if request.method == "POST":
        category = request.POST['category']
        url = 'https://api.chucknorris.io/jokes/random?category='+category

    res = requests.get(url)
    json_data = res.json()

    jokes = {
        "joke": str(json_data["value"])
    }

    return render(request,'weather/CNjokes.html', {'jokes': jokes, 'categories': categories})


