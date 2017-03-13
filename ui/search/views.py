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
import grapher

NOPREF_STR = 'Leave Blank'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
        hero_name='Hero Name',
        alias = 'Alias',
        ID='ID',
        align='Alignment',
        eye='Eye Color',
        hair='Hair Color',
        sex='Sex',
        gsm='Gender/Sexual Minority',
        alive='Alive/Dead',
        appearances='No. of Appearances',
        first_appearance='First Appearance',
)

def _load_column(filename, col=0):
    """Loads single column from csv file"""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)

def _load_res_column(filename, col=0):
    """Load column from resource directory"""
    return _load_column(os.path.join(RES_DIR, filename), col=col)

def _build_dropdown(options):
    """Converts a list to (value, caption) tuples"""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

class IntegerRange(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
                  forms.IntegerField())
        super(IntegerRange, self).__init__(fields=fields,
                                           *args, **kwargs)
    def compress(self, values):
        if values and (values[0] is None or values[1] is None):
            raise forms.ValidationError('Error in Attribute Search (Integer Range): Must specify both lower and upper '
                                        'bound, or leave both blank.')
        if values and (values[1] < values[0]):
            raise forms.ValidationError('Error in Attribute Search: Lower bound must not exceed upper bound.')        

        return values

class AppearanceRange(IntegerRange):
    def compress(self, values):
        super(AppearanceRange, self).compress(values)

    def compress(self, values):
        if values and (values[0] < 0 or values[1] < 0):
            raise forms.ValidationError('Error in Attribute Search: No. of Appearances cannot be negative')

        return values

class Year(IntegerRange):
    def compress(self, values):
        super(Year, self).compress(values)

        if values and (values[0] < 1900 or values[1] > 2017):
            raise forms.ValidationError('Error in Attribute Search: First Appearance must be after 1900 and before 2017')

        return values


RANGE_WIDGET = forms.widgets.MultiWidget(widgets=(forms.widgets.NumberInput,
                                                  forms.widgets.NumberInput))


UNIVERSE = _build_dropdown(['Marvel', 'DC'])
IDENTITY = _build_dropdown(_load_res_column('ID.csv'))
GSM = _build_dropdown(_load_res_column('gsm_list.csv'))
EYE_COLOR = _build_dropdown(_load_res_column('eye_color.csv'))
ALIGNMENT = _build_dropdown(_load_res_column('alignment.csv'))
HAIR_COLOR = _build_dropdown(_load_res_column('hair_color.csv'))
SEX = _build_dropdown(_load_res_column('sex.csv'))

class SearchForm(forms.Form):
    universe = forms.TypedChoiceField(label='Comic Universe',
                                      coerce=lambda x: x=='True',
                                      choices=((False, 'Marvel'), 
                                        (True, 'DC')),
                                      required=False)

    show_attributes = forms.BooleanField(label='Search by Attributes',
                                         required=False)
    query = forms.CharField(
            label='Character Name',
            required=False)

    grapher = forms.TypedChoiceField(label='Network Graph',
                                     help_text=' Warning: Graph may take a long time to load',
                                  coerce=lambda x: x=='True',
                                  choices=((False, 'No'), (True, 'Yes')),
                                  required=False)
    nodes = forms.IntegerField(label=' Max no. of Edges',
                                min_value=0,
                                required=False)
    wiki = forms.TypedChoiceField(label='Wiki Information',
                                  coerce=lambda x: x=='True',
                                  choices=((False, 'No'), (True, 'Yes')),
                                  required=False)

    appearance = AppearanceRange(
        label='No. of Appearances',
        widget=RANGE_WIDGET,
        required=False)

    year = Year(
        label='First Appearance (Year)',
        widget=RANGE_WIDGET,
        required=False)

    show_args = forms.BooleanField(label='Show args_to_ui', #for debugging#
                                   required=False)#
    gsm = forms.MultipleChoiceField(label='Gender/Sexual Minority',
                                    choices=GSM,
                                    widget=forms.CheckboxSelectMultiple,
                                    required=False)
    iden = forms.MultipleChoiceField(label='Identity',
                                     choices=IDENTITY,
                                     widget=forms.CheckboxSelectMultiple,
                                     required=False)
    align = forms.MultipleChoiceField(label='Alignment',
                                     choices=ALIGNMENT,
                                     widget=forms.CheckboxSelectMultiple,
                                     required=False)
    eye = forms.MultipleChoiceField(label='Eye Color',
                                    choices=EYE_COLOR,
                                    widget=forms.CheckboxSelectMultiple,
                                    required=False)
    hair = forms.MultipleChoiceField(label='Hair Color',
                                    choices=HAIR_COLOR,
                                    widget=forms.CheckboxSelectMultiple,
                                    required=False)
    sex = forms.MultipleChoiceField(label='Sex',
                                    choices=SEX,
                                    widget=forms.CheckboxSelectMultiple,
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
            if form.cleaned_data['show_attributes']:
                context['attributes'] = True
            args = {}
            if form.cleaned_data['universe']: #dc
                args['universe'] = 1
            else: #marvel
                args['universe'] = 0
            if form.cleaned_data['query']:
                hero = form.cleaned_data['query']
                args['name'] = hero #538 CSV Data
                api_result = apicall(hero) #Marvel API Data
                desc = api_result[0]
                context['desc_title'] = hero.title()
                context['desc'] = text.wrap((desc), width=170)
                if api_result[1] == 1:
                    context['img'] = True
                wiki_info = form.cleaned_data['wiki'] #Wiki Scraper
                if wiki_info:
                    context['wiki'] = scraper(hero)
                graph = form.cleaned_data['grapher']
                if graph:
                    node = form.cleaned_data['nodes']
                    if node:
                        result = grapher.get_network(hero,node)
                    else:
                        result = grapher.get_network(hero)
                    if result[0] == 1:
                        context['grapher'] = True
                        context['grapher_info'] = result
                        if result[3]:
                            context['grapher_lim'] = True  
            identity = form.cleaned_data['iden']
            if identity:
                args['ID'] = identity
            alignment = form.cleaned_data['align']
            if alignment:
                args['align'] = alignment
            sex = form.cleaned_data['sex']
            if sex:
                args['sex'] = sex
            eye_color = form.cleaned_data['eye']
            if eye_color:
                args['eye'] = eye_color
            hair_color = form.cleaned_data['hair']
            if hair_color:
                args['hair'] = hair_color
            appearances = form.cleaned_data['appearance']
            if appearances:
                args['appearances_lower'] = appearances[0]
                args['appearances_upper'] = appearances[1]
            year = form.cleaned_data['year']
            if year:
                args['year_lower'] = year[0]
                args['year_upper'] = year[1]                
            gsm = form.cleaned_data['gsm']
            if gsm:
                args['gsm'] = gsm            
            if form.cleaned_data['show_args']:
                context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)
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
