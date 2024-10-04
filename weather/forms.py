from django import forms


class GuessForm(forms.Form):
    guess = forms.IntegerField(min_value=1, max_value=100, label='Your Guess')

    guess.widget.attrs.update({"class": "mb-5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg "
        "focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 "
        "dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"})