import random
from jose import jws
from pprint import pprint as pp
import json

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

# Verify & Decode JWS or JWT
def verifyJWS(token, publicCert):
    pemfile = open(publicCert, 'r')
    keystring = pemfile.read()
    pemfile.close()
    payload = jws.verify(token, keystring,  algorithms=['RS256'])
    pp(payload)
    payload = json.loads(payload.decode('utf8'))
    pp(payload)
    return payload