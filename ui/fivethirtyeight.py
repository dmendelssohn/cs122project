import sqlite3
import json
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'fivethirtyeight_marvel.db')

d1 = {'name': ['name'],
      'ID': ['name', 'ID'],
      'ALIGN': ['name', 'ALIGN'],
      'EYE': ['name', 'EYE'],
      'HAIR': ['name', 'HAIR'],
      'SEX': ['name', 'SEX'],
      'ALIVE': ['name', 'ALIVE'],
      'APPEARANCES': ['name', 'APPEARANCES'],
      'FIRST APPEARANCES': ['name', 'FIRST APPEARANCES'],
      'YEAR': ['name', 'YEAR']}

d2 = {'name': (1, 'name'),
      'ID': (2, 'ID'),
      'ALIGN': (3, 'ALIGN'),
      'EYE': (4, 'EYE'),
      'HAIR': (5, 'HAIR'),
      'SEX': (6, 'SEX'),
      'ALIVE': (7, 'ALIVE'),
      'APPEARANCES': (8, 'APPEARANCES'),
      'FIRST APPEARANCES': (9, 'FIRST APPEARANCES'),
      'YEAR': (10, 'YEAR')}

def determine_attributes(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns a list of 
    attributes needed for SQL query
    '''
    attribute_set = set()
    attribute_tuples = []
    attributes = []   

    for key in args_from_ui:
      for attribute in d1[key]:
        attribute_set.add(attribute)

    for attribute in attribute_set:
      attribute_tuples.append(d2[attribute])

    attribute_tuples.sort()

    for attribute in attribute_tuples:
      attributes.append(attribute[1])

    return attributes

def where(args_from_ui):
  '''
  Takes search terms and returns WHERE clause in SQL query and parameters

  e.g. WHERE word IN (?, ?), param = ['economics', 'physical']
  '''
  params = []
  s = ' WHERE '
  for arg in args_from_ui:
    if s != ' WHERE ':
      s += ' AND '
    s += arg + ' = ?'
    params.append(args_from_ui[arg])

  return (s, params)

def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)

def clean_header(s):
    '''
    Removes table name from header
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break

    return s

def find_attributes(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns 
    marvel character information that match the criteria.  The dictionary
    will contain some of the following fields:

      - name (str) e.g. Spider-Man (Peter Parker)
      - ID (str) e.g. 'Secret Identity' or 'Public Identity'
      - Align (str) e.g 'Good Characters' or 'Neutral Characters'
      - Eye (str) e.g. 'Hazel Eyes'
      - Hair (str) e.g. 'Brown Hair'
      - Sex (str) e.g. 'Male Characters'
      - Alive (str) e.g. 'Alive Characters'
      - Appearances (int) e.g. 4043
      - First Appearance (str) e.g. 'Oct-74'
      - Year (int) e.g. 1941
    '''

    # replace with a list of the attribute names in order and a list
    # of query results.

    attributes = determine_attributes(args_from_ui)

    if attributes == []:
      return ([], [])

    attribute_string = ", ".join(attributes)
    where_clause, params = where(args_from_ui)   

    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()

    S = 'SELECT ' + attribute_string + ' FROM marvel' + where_clause 
    query = cursor.execute(S, params)     

    result = query.fetchall()
    header = get_header(query)
    connection.close()

    if result == []:
      return ([], [])
    return(header, result)  
    #return (result)    