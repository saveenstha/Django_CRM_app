from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'economicsapp/index.html')

def EIR(request):

    return render(request, 'economicsapp/effective_interest_rate.html')