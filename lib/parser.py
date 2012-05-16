import re, sys
from glob import glob
from os import getcwd, chdir


def parse(file_to_parse, file_to_save, records_to_create):
  if records_to_create > 1000:
    raise Exception('Records must be <= 1000')
  
  # Templates
  table_template = '''DROP TABLE IF EXISTS {{table_name}};
CREATE TABLE {{table_name}} (
{{table_def}}
);'''

  insert_template = '''INSERT INTO {{table_name}} ({{table_cols}}) VALUES ({{values}});'''


  # Preload the data in the lists folder
  values = {}       # This will make it easier to grab the @command type and a value
  cwd = getcwd()    # Preserve the current working directory
  chdir('./lists')

  filenames = glob('*.txt')
  for filename in filenames:
    value_type = filename[0:filename.find('.')]   # We want to use just the filename without the .txt
    values[value_type] = []
    
    with open(filename, 'r') as file:
      for line in file:
        values[value_type].append(line.replace('\n', ''))

  chdir(cwd)



  # Load the SQL file and save it's contents
  contents = ''
  try:
    with open(file_to_parse, 'r') as file:
      contents = file.read()
  except IOError:
    raise IOError('Schema file not found (-i ' + file_to_parse + ')')
    

  # Use a regular expression to parse the SQL saved in the contents variable
  match = re.findall(r'\s?create\stable\s?(\w+)\s?\(\s?([\w ,\n\(\)@]+)\s?\)\s?;', contents, re.I)

  if not match:
    raise SyntaxError('Invalid schema. Check your SQL.')


  # Begin interating through the array of tuples returned by re.findall
  for group in match:
    insert_actions, table_cols = {}, []
    
    tableT = table_template.replace('{{table_name}}', group[0])
    insertT = insert_template.replace('{{table_name}}', group[0])
    
    statements = [d.strip() for d in group[1].replace('\n', '').split(',')]
    
    # We need to tokenize each table statement to find any @commands to use 
    # when creating the INSERT statements
    for idx, statement in enumerate(statements):
      tokens = statement.split()
      
      for token in tokens:
        if token.find('@') == 0:
          insert_actions[tokens[0]] = token[1:]
          tokens.remove(token)
        
      statements[idx] = ' '.join(tokens)
      
    for col in insert_actions.keys():
      table_cols.append(col)
    
    
    # Write the schema to disc
    with open(file_to_save, 'a') as file:
      file.write(tableT.replace('{{table_def}}', ',\n'.join(statements)) + '\n')
      
      for x in xrange(records_to_create):
        insert_values = []
        for v in insert_actions.values():
          insert_values.append("'" + values[v][x].replace("'", "''") + "'")
        
        file.write(insertT.replace('{{table_cols}}', ', '.join(table_cols)).replace('{{values}}', ', '.join(insert_values)) + '\n')