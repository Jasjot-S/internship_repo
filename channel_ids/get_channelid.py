'''
make a flask api which takes channelids list as input and stores them in redisqueue.
for example you receive channels from api as(accept data in body from api) -
                 {"channelids" : ["channel1", "channel2"]}
dictionary of list with channelids as the key. 
                 
store them in redisqueue as - {"channel" : channel1}
                              {"channel" : channel2}

Create an object of the RedisQueue class, then use the ".put()" method of the class. The data
to be put into the queue should be sent in json format using "json.dumps()" 
image captioning
'''

import redis
from flask import *
import RedisQueue
import json
import config

app = Flask(__name__)

def queue_object():
    queue_obj = RedisQueue.RedisQueue('channelid_object',
		host=config.host,
		port=config.port,
		password=config.password,
		db=config.db
	)
    return queue_obj


@app.route("/send_dat", methods = ['POST'])
def dat_in_queue():

    try:
        dat = request.get_json()
        queue_ob = queue_object()
        for i in dat['channelids']:
            queue_ob.put(json.dumps({"channel" : i}))
        return {"status": True, "code": 200, "message": "Succesfully added to queue" }
    except:
        return {"status" : False, "code" : 404, "message": "Some error occured"}       
        


if __name__ == '__main__':
    app.run(debug = 'True')
