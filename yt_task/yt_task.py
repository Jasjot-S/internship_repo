
from youtubesearchpython import *
import pandas as pd
import psycopg2
import psycopg2.extras
import config

vid_id = '''D81WgY3U_34
3LXTGVN3ZOg
F_7mwIHqtV0
GAJosDLcrf4
ozTAq_iG2hg
-spn9ehbMcA
Mmayd4e85Eo
H2OMJS3iP_U
INw2L_si4KY
tHoqL7cF1pg
o9oLp7o8WAU
42eDO7OjlUI
6rL8Ea6vB8E
dHTSmAf9Szc
Uo_bV9Zobfg
4ZDR3-_qnp4
txlt62Wm9BQ
wEvbAnGPE5Q
NdBeDwLpIcI
YPGK5brPoJ8
O40_MBePNPE
ZTAUuu7MYog
JWhWGy8AKnE
TtMnOkiwhAU
Im84KYtR1gQ
F7yI_ey4AVM
gR89EX2IuS0
IN6ZuXBA_Bo
X2QSAnFOeuY
56vmC1Q0_JE
8yUXj9xmALw
mtKhLgd9yoA
KeNYoM97tkc
tj8OS4MylCI
m6Q763QBF3g
P_m4IOoa6Hc
KCyn6M-nDRI
r5qZoT6bbJo
NSRY_aYmfFo
DnGOsM2drdc
O7iJ7uc5d78
sQYzY-0kc0I
c2c2SGByyL8
fe6ovwhJmHw
JYqenvkFPwQ
soJrg_CjaXI
27CkIneK5n0
GWDHTWFhiuk
Strjq-WZF7Y
g_pjZ5MOhIk
HU4AOdefDzE
K7ns34nR6YQ
yjMvH_Za7hY
m3NesDnKynA
5F5TiFyzlQo
rtxq_tKdMwc
K6e8-eDrCdw
iMi2EzfHOqM
zvBQS9YB5wg
eNpxrXvAm-0
fGJ-6pqvLLw
pHmMe15LOQw
7vTdylBGJKU
JXSx6kLbZN4
XppW9nlFrz4
n7SQoSEs6jo
qFbd_R8uHeI
R4JUK2AdVOc
a1I8xcKuZj8
GUKt1tGShRo
KTgCy0UkbcA
ZkHtK33QdU0
fw5Pe9S87TU
r4N8pD9vXQs
6jif0pSUWWM
JVpo3CfCxxk
0ku5ZFfsPRM
sIaWn3-Zt4U
MQb-PRRUmlg
oQhszMXYVi8
jsbtNK-ndtc
X2WTwrFf2Q4
3j9IXqLvEAY
HTFQaJnQ4AA
jBv349GyBM8
JZACjPYWirw
FnZiaagXtkk
EtTbbzpHeFs
c-TxhvJPlW8
cjWyx_WeV5U
BdWoQW7utvc
c6GCFvuBIME
CJ60R0EZjug
sz_FOPYFJyQ
PJs8smK6DSQ
RXh99gnj3no
7bvUM-mVAEc
7_ytsE1YE48
xSlMWIrQphI
MUpH5Eic7aM'''
vid_ids = vid_id.split('\n')
del (vid_ids[-1])

con = psycopg2.connect(host=config.host,
                       port=config.port,
                       dbname = config.dbname,
                       password = config.password,
                       user = config.user)

cur = con.cursor()

insert_query = """INSERT INTO yt_new_data (vid, publishdate, channelid, title, description, thumbnails, channeltitle,
                                           tags, category, videourl, viewcount, country, commentcount, duration, is_caption) 
                                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

def insert_dat(data_lst):

    print ('In insert')
    for x in data_lst:
         cur.execute(insert_query, x)
         con.commit()
         print("One row done")
    


def create_dat(url):
    flag_com = 0
    flag_tran = 0
    print('Creating data please wait')
    print(url)
    tmp_lst = []

    try: 
        vid_dat = Video.getInfo(url)
    except:
        return {"status" : False, "result" : url}
        

    chan_dat = Channel.get(vid_dat['channel']['id'])

    try: 
        comments = Comments(url)
    except:
        flag_com = 1
        pass
    
    try:
        transpt = Transcript.get(url)
    except:
        flag_tran = 1
        pass

    tmp_lst.append(url)
    tmp_lst.append(vid_dat['publishDate'])
    tmp_lst.append(vid_dat['channel']['id'])
    tmp_lst.append(vid_dat['title'])
    tmp_lst.append(vid_dat['description'])
    lng =  len(vid_dat['thumbnails'])
    tmp_lst.append(vid_dat['thumbnails'][lng - 1]['url'])
    tmp_lst.append(vid_dat['channel']['name'])
    tmp_lst.append(str(chan_dat['tags']))
    tmp_lst.append(vid_dat['category'])
    tmp_lst.append(vid_dat['link'])
    tmp_lst.append(vid_dat['viewCount']['text'])
    tmp_lst.append(chan_dat['country'])
    
    if flag_com == 0:
        tmp_lst.append(len(comments.comments['result']))
    elif flag_com == 1:
        tmp_lst.append(0)
    
    tmp_lst.append(vid_dat['duration']['secondsText'])

    if flag_tran == 0:
        if len(transpt['segments']) == 0 and len(transpt['languages']) == 0:
            is_caption = False
        elif len(transpt) > 0:
            is_caption = True
    elif flag_tran == 1:
        is_caption = False

    tmp_lst.append(is_caption)
    return {"status" : True, "result" : tuple(tmp_lst)}


def main():
    dat_lst = []
    inv_lst = []
    for x in vid_ids:
        tmp_dat = create_dat(x)

        if tmp_dat['status'] == False:
            inv_lst.append(tmp_dat['result'])
            continue
        elif tmp_dat['status'] == True:
            dat_lst.append(tmp_dat['result'])
    

    # print(len(dat_lst))
    insert_dat(dat_lst)
    print("Data transfer successful")
    con.close()


if __name__ == '__main__':
    main()

