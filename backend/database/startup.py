#startup script
#get data from website?
#convert csv to sql insertion
import bz2

with open('sql-scripts/InsertData.sql', 'w') as sqlFile:
    with bz2.open('./data/2008.csv.bz2') as file:
        line = file.readline()
        line = file.readline().decode('utf-8')[:-1] #remove \n at end of line
        #mid = [x if x != '' else '0' for x in line.replace('NA', '0').split(',')]
        #sqlFile.write('INSERT INTO flights VALUES (' + \
        #                       ','.join([x if x.isnumeric() else "'" + x + "'" for x in mid]) + ')\n')
        #line = file.readline().decode('utf-8')[:-1] #remove \n at end of line
        while line:
            mid = [x if x != '' else '0' for x in line.replace('NA', '0').split(',')]
            sqlFile.write('INSERT IGNORE INTO flights VALUES (' + ','.join([x if x.isnumeric() else "'" + x + "'" for x in mid]) + ');\n')
            #sqlFile.write(',(' + ','.join([x if x.isnumeric() else "'" + x + "'" for x in mid]) + ')\n')
            line = file.readline().decode('utf-8')[:-1] #remove \n at end of line
            break
        #sqlFile.write(';\n')
