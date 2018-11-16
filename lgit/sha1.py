import hashlib

def sha1(filepath):
    with open(filepath,'r') as f:
        return hashlib.sha1(f.read().encode()).hexdigest()