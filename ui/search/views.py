from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
import traceback
from io import StringIO
import sys
import csv
import os
from operator import and_
from fivethirtyeight import find_attributes
from functools import reduce

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
        name='Name',
        ID='ID',
        ALIGN='Align',
        EYE='Eye',
        HAIR='Hair',
        SEX='Sex',
        ALIVE='Alive',
        APPEARANCES='Appearances',
        FIRST_APPEARANCES='First Appearances',
        YEAR='Year'
)


class SearchForm(forms.Form):
    query = forms.CharField(
            label='Character Name',
            help_text='e.g. Spider-Man (Peter Parker)',
            required=False)
    show_args = forms.BooleanField(label='Show args_to_ui',
                                   required=False)


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
                args['name'] = form.cleaned_data['query']
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
