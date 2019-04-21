import contract
import random
import time
import json
import hashlib
import requests
# record=[]

def update(cv):
    eventid=str(time.time())
    exp=str(time.time()+random.random()*5+5)

    user1="0x4ccd5762896ae5075808b2cd03599d487e1f33e0"
    user2="0x13af759d94420d097c63d0b4e521d01486b2a4fe"

    level=["is-primary","is-danger","is-info","is-warning"][random.randint(0,3)]
    name=["surpass","compete","opposite"][random.randint(0,2)]
    decider=["human","car"][random.randint(0,1)]
    status=""
    userlevel=str(random.randint(0,10))
    price=str(random.randint(0,500))

    gps="GPRMC,080655.00,A,4546.40891,N,12639.65641,E,1.045,328.42,170809,,,A*60"
    gps="GPRMC,{},A,{},N,{},E,1.045,328.42,170809,,,A*60".format(int(time.time()),4546.40891+5*time.time(),12639.65641+5*time.time())
    gps=[random.random()*100,random.random()*100]
    sensorcv=cv

    event=[{
        "type":"new",
        "event":{
            "id":eventid,
            "from":user1,
            "to":user2,
            "price":price,
            "type":{
                "level":level,
                "name":name
            },
            "expire":exp,
            "decider":decider,
            "status":status,
            "userlevel":userlevel
        },
        "data":{
            "gps":gps,
            "sensorcv":sensorcv
        }
    }]

    event=json.dumps(event)
    r=requests.post("http://api.v.noinfinity.top/event",event)
    contract.update(hashlib.md5(event.encode()).hexdigest(),user1)

    
    time.sleep(3)
    status=["accept","reject"][random.randint(0,1)]

    event=[{
        "type":"update",
        "event":{
            "id":eventid,
            "from":user1,
            "to":user2,
            "price":price,
            "type":{
                "level":level,
                "name":name
            },
            "expire":exp,
            "decider":decider,
            "status":status,
            "userlevel":userlevel,
        
            "data":{
                "gps":gps,
                "sensorcv":sensorcv
            }
        }
    }]

    event=json.dumps(event)
    r=requests.post("http://api.v.noinfinity.top/event",event)
    contract.update(hashlib.md5(event.encode()).hexdigest(),user1)

