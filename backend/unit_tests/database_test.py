#from database.startup import convert_csv
import bz2
from os import listdir
from os.path import isfile, join
import re
import csv
import filecmp

# Check is string can be converted to float
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def convert_csv(dir):
    # get all files in data directory
    datafiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    for datafile in datafiles:
        #bz2 file which should be flights data
        if 'bz2' in datafile:
            year = datafile.split('.')[0]
            newfile = './sql-scripts/Insert' + year + '.sql'
            with open(newfile, 'w') as sqlFile: #file to write to
                with bz2.open(join(dir, datafile)) as file: #file where data is located
                    line = file.readline()
                    line = file.readline().decode('utf-8')[:-1] #remove \n at end of line
                    while line:
                        mid = [x if x != '' else 'NULL' for x in line.replace('NA', '0').split(',')]
                        #print(','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]))
                        sqlFile.write('INSERT IGNORE INTO flights VALUES (' + ','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]) + ');\n')
                        #sqlFile.write(',(' + ','.join([x if x.isnumeric() else "'" + x + "'" for x in mid]) + ')\n')
                        line = file.readline().decode('utf-8')[:-1] #remove \n at end of line

        elif '.csv' in datafile: #csv file
            filename = datafile.split('.')[0]
            if 'plane' in filename:
                filename = 'planes'
            newfile = './sql-scripts/Insert' + filename + '.sql' 
            with open(newfile, 'w') as sqlFile:
                with open(join(dir, datafile), encoding='utf-8') as file:
                    reader = csv.reader(file, quotechar='"')
                    length = len(next(reader))
                    #print(length)
                    for row in reader:
                        line = [x if x != 'NA' else '0' for x in row]
                        mid = [x if x != '' else 'NULL' for x in line]
                        while len(mid) < length:
                            mid.append('NULL')
                        #print(','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]))
                        sqlFile.write('INSERT IGNORE INTO ' + filename + ' VALUES (' + ','.join([x if (is_float(x) or x == 'NULL') else '"' + x + '"' for x in mid]) + ');\n')

def test_convert_csv():
    convert_csv('./test_data/')

#correct_output = INSERT IGNORE INTO testdata VALUES ("00M","Thigpen,sa'd ",0,"MS","USA",31.95376472,-89.23450472);

with open('./sql-scripts/Inserttestdata.sql', 'rb') as file:
    assert filecmp.cmp('./sql-scripts/Inserttestdata.sql', './sql-scripts/correct.sql')