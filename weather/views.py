from django.shortcuts import render
from django.http import Http404
import requests
import random
import json
import urllib.request
from urllib.error import HTTPError
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from .forms import GuessForm
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


class RandomNumberGuess(View):
    template_name = 'weather/game.html'

    def get(self, request):
        # If the game has not started, initialize the number and attempts
        if 'number_to_guess' not in request.session:
            request.session['number_to_guess'] = random.randint(1, 100)
            request.session['attempts'] = 0

        form = GuessForm()
        return render(request, self.template_name, {
            'form': form,
            'message': 'Guess a number between 1 and 100',
            'attempts': request.session['attempts']
        })

    def post(self, request):
        form = GuessForm(request.POST)

        # Load the correct number and attempts from the session
        number_to_guess = request.session['number_to_guess']
        attempts = request.session['attempts']

        if form.is_valid():
            guess = form.cleaned_data['guess']
            attempts += 1

            if guess > number_to_guess:
                message = "Your guess is too high! Try again."
            elif guess < number_to_guess:
                message = "Your guess is too low! Try again."
            else:
                message = f"Congratulations! You guessed the correct number in {attempts} attempts."
                # Reset the game (clear session)
                del request.session['number_to_guess']
                del request.session['attempts']

            # Update attempts in the session
            request.session['attempts'] = attempts
        else:
            message = "Invalid input. Please enter a number between 1 and 100."

        return render(request, self.template_name, {
            'form': form,
            'message': message,
            'attempts': attempts
        })
