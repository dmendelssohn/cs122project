import sqlite3
import json
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'fivethirtyeight_marvel.db')

d1 = {'name': ['name', 'id', 'align', 'eye', 'hair', 'sex', 'gsm', 'alive',
               'appearances', 'first_appearance', 'year'],
      'id': ['name', 'id'],
      'align': ['name', 'align'],
      'eye': ['name', 'eye'],
      'hair': ['name', 'hair'],
      'sex': ['name', 'sex'],
      'gsm': ['name', 'gsm'],
      'alive': ['name', 'alive'],
      'appearances': ['name', 'appearances'],
      'first_appearance': ['name', 'first_appearance'],
      'year': ['name', 'year']}

d2 = {'name': (1, 'name'),
      'id': (2, 'id'),
      'align': (3, 'align'),
      'eye': (4, 'eye'),
      'hair': (5, 'hair'),
      'sex': (6, 'sex'),
      'gsm': (7, 'gsm'),
      'alive': (8, 'alive'),
      'appearances': (9, 'appearances'),
      'first_appearance': (10, 'first_appearance'),
      'year': (11, 'year')}

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

  e.g. WHERE name = ?, param = ['Spider-Man (Peter-Parker)']
  '''
  params = []
  s = ' WHERE '
  for arg in args_from_ui:
    if s != ' WHERE ':
      s += ' AND '
    if arg == 'name':
      s += arg + ' = ? OR hero_name = ? OR alias = ?' 
      params += [args_from_ui[arg]] * 3
    else:
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
      -'id (str) e.g. 'Secret'identity' or 'Public'identity'
      - align (str) e.g 'Good Characters' or 'Neutral Characters'
      - eye (str) e.g. 'Hazel eyes'
      - hair (str) e.g. 'Brown hair'
      - sex (str) e.g. 'Male Characters'
      - alive (str) e.g. 'alive Characters'
      - appearances (int) e.g. 4043
      - first_appearance (str) e.g. 'Oct-74'
      - year (int) e.g. 1941
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

    S = 'SELECT ' + attribute_string + ' FROM marvel' + where_clause + ' COLLATE NOCASE'
    query = cursor.execute(S, params)     

    result = query.fetchall()
    header = get_header(query)
    connection.close()

    if result == []:
      return ([], [])
    return(header, result)  
    #return (result)    