from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import text 
from django import forms
import json
import traceback
from io import StringIO
import sys
import csv
import os
from operator import and_
from fivethirtyeight import find_attributes
from apicall import apicall 
from PIL import Image
from functools import reduce
from wiki_scraper import scraper

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
        hero_name='Hero Name',
        alias = 'Alias',
        ID='ID',
        align='Alignment',
        eye='Eye Color',
        hair='Hair Color',
        sex='Sex',
        alive='Alive/Dead',
        appearances='No. of Appearances',
        first_appearance='First Appearance',
        year='Year'
)


def _build_dropdown(options):
    """Converts a list to (value, caption) tuples"""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

UNIVERSE = _build_dropdown(['Marvel', 'DC'])
IDENTITY = _build_dropdown(['Secret Identity', 'Public Identity'])

class SearchForm(forms.Form):
    universe = forms.MultipleChoiceField(label='Comic Universe',
                                         choices=UNIVERSE,
                                         widget=forms.CheckboxSelectMultiple,
                                         required=True)
    query = forms.CharField(
            label='Character Name',
            help_text='e.g. Spider-Man',
            required=False)
    wiki = forms.TypedChoiceField(label='Request Wikipedia Information',
                                  coerce=lambda x: x=='True',
                                  choices=((False, 'No'), (True, 'Yes')),
                                  required=False)
    iden = forms.MultipleChoiceField(label='Identity',
                                         choices=IDENTITY,
                                         widget=forms.CheckboxSelectMultiple,
                                         required=False)
    eye = forms.CharField(label='Eye Color',
                          help_text = 'e.g. Hazel',
                          required=False)
    #show_args = forms.BooleanField(label='Show args_to_ui',
    #                               required=False)


def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # Convert form data to an args dictionary for find_attributes
            args = {}
            if form.cleaned_data['query']:
                hero = form.cleaned_data['query']
                args['name'] = hero #538 CSV Data
                api_result = apicall(hero) #Marvel API Data
                desc = api_result[0]
                context['desc'] = text.wrap((desc), width=170)
                if api_result[1] == 1:
                    context['img'] = True
            wiki_info = form.cleaned_data['wiki']
            if wiki_info:
                context['wiki'] = scraper(hero)
            identity = form.cleaned_data['iden']
            if identity:
                args['ID'] = identity
            eye_color = form.cleaned_data['eye']
            if eye_color:
                args['eye'] = eye_color + ' Eyes'
                #image = get_img(form.cleaned_data['query'])
                #image.save('../static', 'JPEG')

            #if form.cleaned_data['show_args']:
            #    context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

            try:
                res = find_attributes(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_attributes:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
        cols = None
    #elif not _valid_result(res):
    #    context['result'] = None
    #    context['err'] = ('Return of find_courses has the wrong data type. '
    #                     'Should be a tuple of length 4 with one string and three lists.')
    else:
        columns, result = res

        # Wrap in tuple if result is not already
        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'index.html', context)
