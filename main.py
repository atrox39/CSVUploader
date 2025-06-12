import csv
import pypyodbc
import dotenv
import os
import re
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser(
  prog='Database CSV Uploader',
  description='Upload multiple CSV Files to SQL Server',
)
parser.add_argument('--export', required=False, help='Export SQL File to execute Manual Querys', default=False)
args = parser.parse_args()

dotenv.load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
CSV_PATH = os.getenv('CSV_PATH')
FILE_PATTERN = os.getenv('FILE_PATTERN')
FILE_SPLITTER = os.getenv('FILE_SPLITTER')

DB_STRING = 'Driver={{ODBC Driver 17 for SQL Server}};Server={0};Database={1};UID={2};PWD={3}'.format(
  DB_HOST,
  DB_NAME,
  DB_USER,
  DB_PASS,
)

def save_line_log(log, logname):
  if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
    os.mkdir(os.path.join(os.getcwd(), 'logs'))
  logpath = os.path.join(os.getcwd(), 'logs')
  logname = os.path.join(logpath, logname)
  with open(logname, '+a') as file:
    file.write(log+'\n')

def save_script(script, scriptname):
  if not os.path.exists(os.path.join(os.getcwd(), 'scripts')):
    os.mkdir(os.path.join(os.getcwd(), 'scripts'))
  scriptpath = os.path.join(os.getcwd(), 'scripts')
  scriptname = os.path.join(scriptpath, scriptname)
  with open(scriptname, '+a') as file:
    file.write(script)

def parse_value(value):
  if value.isnumeric():
    return str(value)
  return "'" + value + "'"

def get_files():
  files = []
  for file in os.listdir(os.path.join(os.getcwd(), CSV_PATH)):
    if re.match(FILE_PATTERN, file):
      files.append(file)
  return files

def create_query(tablename, columns, row) -> str:
  query = 'INSERT INTO ' + tablename + ' '
  for indexColumn in range(0, len(columns)):
    if indexColumn == 0:
      query += '(' + columns[indexColumn]
    elif indexColumn == len(columns) - 1:
      query += ', ' + columns[indexColumn] + ')'
    else:
      query += ', ' + columns[indexColumn]
  for i in range(len(row)):
    if i == 0:
      query += ' VALUES (' + parse_value(row[i])
    elif i == len(row) - 1:
      query += ', ' + parse_value(row[i]) + ')'
    else:
      query += ', ' + parse_value(row[i])
  return query

def upload_data(filename, table):
  logfile = time.strftime("%Y%m%d-%H%M%S") + '.log'
  if args.export:
    scriptname = time.strftime("%Y%m%d-%H%M%S") + '.sql'
  conn = pypyodbc.connect(DB_STRING)
  cursor = conn.cursor()
  with open(filename, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    columns = []
    for row in csv_reader:
      if count == 0:
        columns = row
        count += 1
        continue
      query = create_query(table, columns, row)
      try:
        if args.export:
          save_script(query + ';\n', scriptname)
        else:
          cursor.execute(query)
          conn.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        print('{} seconds'.format(time.time() - start_time))
      except Exception as e:
        save_line_log(str(e) + ' | SQL Query: ' + query, logfile)
      count += 1
    file.close()
  cursor.close()
  conn.close()

if __name__ == '__main__':
  files = get_files()
  for file in files:
    tablename = file.split(FILE_SPLITTER)[0]
    upload_data(os.path.join(os.getcwd(), CSV_PATH, file), tablename)
