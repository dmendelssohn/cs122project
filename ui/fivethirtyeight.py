import sqlite3
import json
import os
import apicall


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'fivethirtyeight.db')

d1 = {'name': ['hero_name', 'alias',
      'ID', 'align', 'eye', 'hair', 'sex', 'gsm', 'alive',
      'appearances', 'first_appearance'],
      'ID': ['hero_name', 'alias', 'ID'],
      'align': ['hero_name', 'alias', 'align'],
      'eye': ['hero_name', 'alias', 'eye'],
      'hair': ['hero_name', 'alias', 'hair'],
      'sex': ['hero_name', 'alias', 'sex'],
      'gsm': ['hero_name', 'alias', 'gsm'],
      'alive': ['hero_name', 'alias', 'alive'],
      'appearances_lower': ['hero_name', 'alias', 'appearances'],
      'appearances_upper': ['hero_name', 'alias', 'appearances'],
      'appearances': ['hero_name', 'alias', 'appearances'],
      'first_appearance': ['hero_name', 'alias', 'first_appearance'],
      'year_lower': ['hero_name', 'alias', 'first_appearance'],
      'year_upper': ['hero_name', 'alias', 'first_appearance'],
      'universe': []}

d2 = {'hero_name': (1, 'hero_name'),
      'alias': (2, 'alias'),
      'ID': (3, 'ID'),
      'align': (4, 'align'),
      'eye': (5, 'eye'),
      'hair': (6, 'hair'),
      'sex': (7, 'sex'),
      'gsm': (8, 'gsm'),
      'alive': (9, 'alive'),
      'appearances': (10, 'appearances'),
      'first_appearance': (11, 'first_appearance'),
      'year': (12, 'year')}

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

def get_from_clause(args_from_ui):
  '''
  Takes a dictionary containing key-value:
    'universe': 0 or 1
  and returns a string 'FROM marvel' if 0
                       'FROM dc' if 1
  '''
  if args_from_ui['universe'] == 0:
    return ' FROM marvel'
  else:
    return ' FROM dc'

def where(args_from_ui):
  '''
  Takes search terms and returns WHERE clause in SQL query and parameters

  e.g. WHERE name = ?, param = ['Spider-Man (Peter-Parker)']
  '''
  params = []
  s = ' WHERE '
  for arg in args_from_ui:
    if not arg == 'universe':
      if s != ' WHERE ':
        s += ' AND '
      if arg == 'name':
        s += '(' + arg + ' = ? COLLATE NOCASE OR hero_name = ? COLLATE NOCASE OR alias = ? COLLATE NOCASE)' 
        params += [args_from_ui[arg]] * 3
      elif arg == 'appearances_lower':
        s += 'appearances >= ?'
        params.append(args_from_ui[arg])
      elif arg == 'appearances_upper':
        s += 'appearances <= ?'
        params.append(args_from_ui[arg])
      elif arg == 'year_lower':
        s += 'year >= ?'
        params.append(args_from_ui[arg])
      elif arg == 'year_upper':
        s += 'year <= ?'
        params.append(args_from_ui[arg])
      else:
        if arg != []:
          s += arg + ' IN ('
          for entry in args_from_ui[arg]:
            s+= '?'
            if entry != args_from_ui[arg][-1]:
              s+= ', '
            params.append(entry)
          s+= ')'

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
      -'ID (str) e.g. 'Secret'Identity' or 'Public'Identity'
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
    from_clause = get_from_clause(args_from_ui)     
    where_clause, params = where(args_from_ui)  

    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()

    S = 'SELECT ' + attribute_string + from_clause + where_clause
    #print(S, params) #for debugging
    query = cursor.execute(S, params)     

    result = query.fetchall()
    header = get_header(query)
    connection.close()

    if result == []:
      return ([], [])
    return(header, result)    