import re, sys
from glob import glob
from os import getcwd, chdir
from os.path import exists, isdir

class SQLParser:
  def __init__(self, file_to_parse, save_as, records_to_create):
    
    # Before we start we're going to create a
    # list of data types that should not be
    # quoted in our INSERT statements.
    self.dont_quote = 'tinyint smallint mediumint integer int bigint decimal'.split()
    
    # Let's keep the arguments around for a
    # bit, shall we?
    self.file_to_parse = file_to_parse
    self.save_as = save_as
    self.records_to_create = records_to_create
    
    # We're also going to need to place our
    # templates somewhere, so why not here?
    self.template = {'table':'''DROP TABLE IF EXISTS {{table_name}};
CREATE TABLE {{table_name}} (
{{table_def}}
);''', 'insert': '''INSERT INTO {{table_name}} ({{table_cols}}) VALUES ({{values}});'''}
    
    # Gonna need a container to hold all of the
    # possible values from the lists folder too.
    self.values = {}
    
    # Gotta make sure the file and directory 
    # are even there.
    self.files_exist()
    
    # Okay, so we're still running which means
    # everything is where it should be. Let's
    # continue by grabbing the decorators and
    # their values.
    self.preload_values()
    
    # "License and registration, sir." Time to
    # get the SQL from the file.
    self.contents = self.load_sql()
    
    # Now that we have the SQL file's contents go
    # ahead and make sure it fits the bill for
    # a schema.
    self.matches = self.sql_integrity()
    
    # Okay, it's go time!
    self.process()
    
    
  def process(self):
    for group in self.matches:
      insert_actions = {}
      
      tableT = self.template['table'].replace('{{table_name}}', group[0])
      insertT = self.template['insert'].replace('{{table_name}}', group[0])
      
      statements = [d.strip() for d in group[1].replace('\n', '').split(',')]
      
      # We need to tokenize each table statement to find any @commands to use 
      # when creating the INSERT statements
      for idx, statement in enumerate(statements):
        tokens = statement.split()
        
        for token in tokens:
          if token.find('@') == 0:
            insert_actions[tokens[0]] = [token[1:]]
            tokens.remove(token)
          
        # List comparison needed to determine
        # if the INSERT data should be quoted.
        #
        # If the length of tokens is one less after the set() subtractions
        # the column shouldn't be quoted.
        if tokens[0] in insert_actions:
          if len(set(tokens) - set(self.dont_quote)) == len(tokens) - 1:
            insert_actions[tokens[0]].append(False)
          else:
            insert_actions[tokens[0]].append(True)
        
        statements[idx] = ' '.join(tokens)
        
      # Write the schema to disc
      with open(self.save_as, 'a') as file:
        file.write(tableT.replace('{{table_def}}', ',\n'.join(statements)) + '\n')
        
        for x in xrange(self.records_to_create):
          insert_values = []
          
          # If the last item in the insert_actions.values()
          # is True we know we need to INSERT that value
          # using quotations.
          for v in insert_actions.values():
            if v[1] == True:
              insert_values.append("'" + self.values[v[0]][x].replace("'", "''") + "'")
            else:
              insert_values.append(self.values[v[0]][x])
          
          file.write(insertT.replace('{{table_cols}}', ', '.join(insert_actions.keys())).replace('{{values}}', ', '.join(insert_values)) + '\n')
  
  
  def files_exist(self):
    if not isdir('./lists'):
      raise IOError('The lists directory cannot be found.')
    
    if not exists(self.file_to_parse):
      raise IOError('Schema file not found (-i ' + self.file_to_parse + ')')
      
    return True
    
    
  def preload_values(self):
    cwd = getcwd()    # Preserve the current working directory
    chdir('./lists')

    filenames = glob('*.txt')
    for filename in filenames:
      value_type = filename[0:filename.find('.')]   # We want to use just the filename without the .txt
      self.values[value_type] = []
      
      with open(filename, 'r') as file:
        for line in file:
          self.values[value_type].append(line.replace('\n', ''))

    chdir(cwd)
    
    
  def load_sql(self):
    contents = ''
    
    with open(self.file_to_parse, 'r') as file:
      contents = file.read()
      
    if len(contents.strip()) < 20:
      raise SyntaxError('Invalid SQL.')
    
    return contents
  
  
  def sql_integrity(self):
    expression = r'\s?create\stable\s?(\w+)\s?\(\s?([\w ,\n\(\)@]+)\s?\)\s?;'
    matches = re.findall(expression, self.contents, re.I)

    if not matches:
      raise SyntaxError('Invalid schema. Check your SQL.')
    
    return matches