import requests

URL = 'http://127.0.0.1:5000/'

# Getting feature importance as list
h1 = {'Content-type': 'application/json', 'Accept': 'application/json'}
# Inputs are for columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
#       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']
params1 = {'inputs': [3, 28, 5, 635, 912, 'YV', 'N956LR', 97.0, 'MEM', 'CLT', 512]}
req = requests.get('http://127.0.0.1:5000/api/lime_fi',headers=h1, json=params1)
#req.text
#output is a list containing feature importance
#e.g. '[["DayOfWeek=5",0.04459373534188866],["CRSDepTime",0.042533720995852516],["Distance",0.022956906602916605],\
# ["DayofMonth=28",-0.02028326218839363],["Dest=CLT",-0.01361981943433478],["Origin=MEM",0.012663409910100145],\
# ["TailNum=N956LR",0.012495320364865902],["Month=3",0.012461212222973975],["UniqueCarrier=YV",-0.01192746105881419],\
# ["CRSArrTime",0.004145908201383367]]\n'

# Getting feature importance with plots as html?
h1 = {'Content-type': 'application/json', 'Accept': 'application/json'}
# Inputs are for columns = ['Month','DayofMonth', 'DayOfWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier',
#       'TailNum', 'CRSElapsedTime', 'Origin', 'Dest', 'Distance']
params1 = {'inputs': [3, 28, 5, 635, 912, 'YV', 'N956LR', 97.0, 'MEM', 'CLT', 512]}
req = requests.get('http://127.0.0.1:5000/api/lime_plot',headers=h1, json=params1)
#req.text
#output is a html string? Need to figure out how to render if using
#'"<html>\\n  ... ... </html>"\n'