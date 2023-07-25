import RedisQueue
import core
import json
import requests
from PIL import Image
import config

def queue_object(name):
    queue_obj = RedisQueue.RedisQueue(name,
		host=config.host,
		port=config.port,
		password=config.password,
		db=config.db
	)
    return queue_obj


def get_channel_queue():

    queue_obj = queue_object('channelid_object')
    video_queue = queue_object('video_queue')

    while(True):
        try:
            if queue_obj.empty():
                print("empty queue")
                break
            else :
                channel = queue_obj.get('channel')
                channel_json = json.loads(channel)
                id = channel_json['channel']
                core_obj = core.ChannelDetails(id, True)
                vals = core_obj.parse_response()
                for i in range(len(vals)):
                    video_queue.put(json.dumps({'vid' : vals['videos'][i]['vid'],
                                                'channel' : vals['channelid'],
                                                'thumbnail' : vals['videos'][i]['thumbnails'] + ".jpg"}))
                  
                print ({'status' : True, 'code': 200, 'message' : "Data added succesfully"})
        except:
            print ({'status' : False, 'code' : 404, 'message' : 'An error has occured'})

            
def get_vid():
    vid_obj = queue_object('video_queue')

    while (True):
        try :
            if vid_obj.empty():
                print ("Queue is empty")
                break
            else:
                dat = vid_obj.get()
                dat = json.loads(dat)
                url = dat['thumbnail']
                vid = dat['vid']
                download_img(url, vid)
                print("Image downloaded successfully")
        except:
            print ("Some error occured")
    

def download_img(url, vid):
    img = requests.get(url).content
    f = open(vid + '.jpg', 'wb')
    f.write(img)
    f.close

if __name__ == '__main__':
    get_channel_queue()
    get_vid()