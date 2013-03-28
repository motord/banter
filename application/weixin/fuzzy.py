__author__ = 'peter'

from hashes.simhash import simhash
from google.appengine.api import memcache

def decide(forktionary, message):
    message_hash=simhash(message.split())
    similarity=0
    val=None
    for key, value in forktionary.iteritems():
        key_hash=memcache.get(key)
        if not key_hash:
            key_hash=simhash(key.split())
            memcache.set(key, key_hash)
            sim=message_hash.similarity(key_hash)
            if sim>similarity:
                similarity=sim
                val=value
    return val


