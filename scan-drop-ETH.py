import requests
import datetime
import sys
import time

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
    if not len(queue) < NUMBER_VALUE:
        queue.pop(0)
    return;
    
def getFallPercentage(first, last):
    return 100 - (last * 100 / first)

# Defaults parametes
FAIL_PERCENTAGE_THRESHOLD=2
NUMBER_VALUE=15

if len(sys.argv) == 2:
    print('Using parameter')
    FAIL_PERCENTAGE_THRESHOLD=sys.argv[0]
    NUMBER_VALUE=sys.argv[1]
    
while True :    
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=EUR&limit=60'
    response = requests.get(url)
    
    queue = list()
    
    for bid in response.json()["Data"]:
        appendToQueue(queue, bid['high'])
        
        fall = getFallPercentage(queue[0], queue[len(queue)-1])
        if fall > FAIL_PERCENTAGE_THRESHOLD:
            print('Fall detected => ', fall)
    time.sleep(3)
    
