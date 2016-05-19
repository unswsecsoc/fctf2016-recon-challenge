from flask import Flask
from flask import request
from app import db
from app import key
import base64
import hashlib

def load_flags():
    print '[+] Loading flags from files'
    global flag1
    with open('flag1.txt') as f:
        flag1 = f.read().strip()

    global flag2
    with open('flag2.txt') as f:
        flag2 = f.read().strip()

def check_currency_cookie():
    result = {'new_currency': 'PKD-P-false', 'new_abbrev': 'PKD', 'new_sym': 'P'}
    if 'currency' in request.cookies:
        oreo = request.cookies['currency'].split('|')
        top_layer = base64.b64decode(oreo[1])
        if (oreo[0] != hash(top_layer.decode('utf-8'))[0:6]):
            raise
        else:
            cream = top_layer.split('-')
            result['new_currency'] = top_layer.decode('utf-8')
            result['new_abbrev'] = cream[0]
            result['new_sym'] = cream[1].decode('utf-8')
    return result
# Create all database tables

def load_currency():
    if 'currency' in request.cookies:
        try:
            reqcurr = check_currency_cookie()
        except:
            print '[-] failed to verify cookie, pls work', request.cookies['currency']
            new_currency = 'AUD-$-false'
            new_abbrev = 'AUD'
            new_sym = '$'
        else:
            print '[-] new cookie', reqcurr
            new_currency = reqcurr['new_currency']
            new_abbrev = reqcurr['new_abbrev']
            new_sym = reqcurr['new_sym']
    else:
            new_currency = 'AUD-$-false'
            new_abbrev = 'AUD'
            new_sym = '$'
    result = {'new_currency': new_currency,
                'new_abbrev': new_abbrev,
                'new_sym': new_sym}
    return result

def hash(string):
    m = hashlib.sha512()
    m.update(key)
    m.update(string.encode('utf-8'))
    return m.hexdigest()
