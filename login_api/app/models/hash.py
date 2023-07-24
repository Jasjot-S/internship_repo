import hashlib 

def get_hash(string):
    tmp = hashlib.md5()
    tmp.update(string.encode('utf-8'))    
    return tmp.hexdigest()

