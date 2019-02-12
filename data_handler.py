from google.cloud import datastore
from datetime import datetime
from pprint import pprint as pp
from security import security
import uuid
import sys

test =  {
            "name":"TAN XIAO HUI",
            "sex": "F",
            "race": "CN",
            "nationality": "SG",
            "dob":"1970-05-17",
            "email": "myinfotesting@gmail.com",
            "mobileno": "+97399245",
            "regadd": "SG, 128 street BEDOK NORTH AVENUE 4 block 102 postal 460102 floor 09 building PEARL GARDEN", 
            "hdbtype":"113",
            "marital": "1",
            "edulevel": "3",
            "assessableincome": "1456789.00",
            "uinfin":"S9812381D"
        }
def validateUserLogin(userName, password):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    query = datastore_client.query(kind='users', namespace='MyInfoApp')
    query.add_filter('password', '=', password)
    query.add_filter('userName', '=', userName)
    users = list(query.fetch())
    pp(users)
    for user in users:
        if user['userName'] == userName and user['password'] == password:
            return True
    return False
def generateSessionEntity():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # Fetch the current date / time.
    current_datetime = datetime.now()

    # The kind for the new entity.
    kind = 'Sessions'

    # The name/ID for the new entity.
    session = uuid.uuid4().hex

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, str(session), namespace='MyInfoApp')

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, requester, requetee, timestamp, nonce.
    entity = datastore.Entity(key)
    entity['requester'] = ""
    entity['requestee'] = ""
    entity['timestamp'] = current_datetime
    entity['data'] = dict()
    entity['nonce'] = security.generate_nonce(15)

    # Save the new entity to Datastore.
    datastore_client.put(entity)
    return session
def updateSessionEntity(session, requester, requestee, data):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = 'Sessions'
    key = datastore_client.key(kind, str(session), namespace="MyInfoApp")
    entity = datastore_client.get(key)
    if entity is None:
        return None
    entity['requester'] = requester
    entity['requestee'] = requestee
    entity['data'] = data
    datastore_client.put(entity)
    return session

def getSessionEntity(session):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = 'Sessions'
    key = datastore_client.key(kind, str(session), namespace="MyInfoApp")
    entity = datastore_client.get(key)
    if entity is None:
        return None
    return entity

def query_data(requester):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = 'Sessions'
    query = datastore_client.query(kind=kind, namespace='MyInfoApp')
    query.add_filter('requester', '=', requester)
    requesters = list(query.fetch())
    if requesters is None:
        return None
    data = [requester['data'] for requester in requesters]
    return data

if __name__ == "__main__":
    sess = generateSessionEntity()
    print(sess)
    entity = getSessionEntity(sess)
    if entity is None:
        sys.exit()
    if entity['requester'] is None:
        pp("requester is none")
    if entity['requester'] == "":
        pp("requester is empty")
    if entity['requestee'] is None:
        pp("requestee is none")
    if entity['requestee'] == "":
        pp("requestee is empty")
    if not entity['data']:
        pp("data is empty")
    sess = updateSessionEntity(sess, "abc", "efg", test)
    print(sess)
    entity = getSessionEntity(sess)
    if entity['requester'] is None:
        pp("requester 2 is none")
    if entity['requester'] != "":
        pp("requester 2 is not empty")
    if entity['requestee'] is None:
        pp("requestee 2 is none")
    if entity['requestee'] != "":
        pp("requestee 2 is not empty")
    if entity['data']:
        pp("data 2 is empty")
    pp(entity)