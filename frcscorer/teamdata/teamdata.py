from faunadb.client import FaunaClient
from faunadb import query as q
from dotenv import load_dotenv
import os

load_dotenv()

client = FaunaClient(
    secret=os.environ['FAUNA_SECRET_KEY'])

# res = client.ping()

# res = client.query(q.get(q.ref(q.collection('Test'), "347563724815467092")))

# ref = client.query(q.select("ref", q.get(q.collection("AllTime"))))

# res = client.query(q.get(q.select('ref', q.get(q.collection('AllTime')))))

# res = client.query(q.get(q.collection('AllTime')))

# res = client.query(q.paginate(q.collection('AllTime')))

res = client.query(q.paginate(q.documents(q.collection('AllTime'))))

print(res)
