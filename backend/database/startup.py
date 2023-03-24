#startup script
#get data from website?
#convert csv to sql insertion
import bz2
from os import listdir
from os.path import isfile, join
import re
import csv

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

datafiles = [f for f in listdir('./data/') if isfile(join('./data/', f))]
for datafile in datafiles:
    if 'bz2' in datafile: #bz2 file
        year = datafile.split('.')[0]
        newfile = './sql-scripts/Insert' + year + '.sql'
        with open(newfile, 'w') as sqlFile:
            with bz2.open(join('./data/', datafile)) as file:
                line = file.readline()
                line = file.readline().decode('utf-8')[:-1] #remove \n at end of line
                while line:
                    mid = [x if x != '' else 'NULL' for x in line.replace('NA', '0').split(',')]
                    #print(','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]))
                    sqlFile.write('INSERT IGNORE INTO flights VALUES (' + ','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]) + ');\n')
                    #sqlFile.write(',(' + ','.join([x if x.isnumeric() else "'" + x + "'" for x in mid]) + ')\n')
                    line = file.readline().decode('utf-8')[:-1] #remove \n at end of line
                    #break
    elif '.csv' in datafile: #csv file
        filename = datafile.split('.')[0]
        if 'plane' in filename:
            filename = 'planes'
        newfile = './sql-scripts/Insert' + filename + '.sql' 
        with open(newfile, 'w') as sqlFile:
            with open(join('./data/', datafile), encoding='utf-8') as file:
                reader = csv.reader(file, quotechar='"')
                length = len(next(reader))
                #print(length)
                for row in reader:
                    line = [x if x != 'NA' else '0' for x in row]
                    mid = [x if x != '' else 'NULL' for x in line]
                    while len(mid) < length:
                        mid.append('NULL')
                    #print(','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]))
                    sqlFile.write('INSERT IGNORE INTO ' + filename + ' VALUES (' + ','.join([x if (is_float(x) or x == 'NULL') else "'" + x + "'" for x in mid]) + ');\n')
                    #line = file.readline()[:-1] #remove \n at end of line
                    #break
                    #break
                # line = file.readline()
                # length = len(line.split(','))
                # line = file.readline()[:-1] #remove \n at end of line
                # line = re.sub(r'"', '', line)
                # while line: #not empty
                #     #print(line.replace('NA', '0'))
                #     mid = [x if x != '' else 'NULL' for x in line.replace('NA', '0').split(',')]
                #     while len(mid) < length:
                #         mid.append('NULL')
                #     #print(','.join([x if (x.isnumeric() or x == 'NULL') else "'" + x + "'" for x in mid]))
                #     sqlFile.write('INSERT IGNORE INTO ' + filename + ' VALUES (' + ','.join([x if (is_float(x) or x == 'NULL') else "'" + x + "'" for x in mid]) + ');\n')
                #     line = file.readline()[:-1] #remove \n at end of line
                #     break
