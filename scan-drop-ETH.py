import requests
import datetime
import sys
import time
import json

'''
INPUT 
   1 arg : FAIL_PERCENTAGE_THRESHOLD
   2 arg : NUMBER_VALUE

DESCRIPTION

This script call cryptocompare API to fetch last ETH price and detect if there is a significant fall

'''

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

def appendToQueue(queue, e):
    queue.append(e)
    if not len(queue) <= NUMBER_VALUE:
        queue.pop(0)
    return;
    
def getFallPercentage(first, last):
    return 100 - (last * 100 / first)

def dateFormat(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Defaults parametes
FAIL_PERCENTAGE_THRESHOLD=2
NUMBER_VALUE=15

if len(sys.argv) == 3:
    FAIL_PERCENTAGE_THRESHOLD=float(sys.argv[1])
    NUMBER_VALUE=int(sys.argv[2])

print('Scanning [ Threshold percentage -> ', FAIL_PERCENTAGE_THRESHOLD, ', Queue size -> ', NUMBER_VALUE, '] ...')

while True :    
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym=ETH&tsym=EUR&limit=60'
    response = requests.get(url)
    maxFall = 0
    queue = list()
    
    for bid in response.json()["Data"]:
        appendToQueue(queue, bid['close'])
        
        fall = getFallPercentage(queue[0], queue[len(queue)-1])
        maxFall = max(fall, maxFall)
        if fall > FAIL_PERCENTAGE_THRESHOLD:
            print('Threshold reached [ Fall off percentage -> ', fall, ', Date of bid -> ', dateFormat(bid['time']))
            url = 'https://api.pushbullet.com/v2/pushes'
            headers = {'Access-Token' : 'o.vlYfChSpf8cJS24OpcHyEAqwg9d3AqwO', 'Content-Type': 'application/json' }
            body = {"type" : "note", "title": "ETH Scan"}
            body["body"] = "Trade has fallen to "+str(fall)
            response = requests.post(url, data=json.dumps(body), headers=headers)
            print(response)
            break

    print('Ending iteration [ Max fall percentage -> ', maxFall, ']')
    time.sleep(60)

