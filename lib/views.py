import sys
from parser import SQLParser
from argparse import ArgumentParser

parser = ArgumentParser(description='SQL generator used to populate a test database based on your own schema.. and some decorators.')

parser.add_argument('-v', '--version', action='version', version='v0.1.0')
parser.add_argument('-i', '--input', dest='input_file', help='The schema file to use.', required=True)
parser.add_argument('-o', '--output', dest='output_file', default='output.sql', help='The name of the file to output your new schema to. (default = output.sql)')
parser.add_argument('-r', '--records', dest='records', default=500, help='The number of records to create for your database. (default = 500, max = 1000)')

args = parser.parse_args()

SQLParser(str(args.input_file), str(args.output_file), int(args.records))
  
  
if __name__ == '__main__':
  print '{0} should not be invoked from the commandline.'.format(sys.argv[0])
  sys.exit(0)