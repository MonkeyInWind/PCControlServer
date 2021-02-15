from fastapi import FastAPI, Query, Body, Cookie, Header, status
from enum import Enum
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from  routes import routerTest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routerTest.router, prefix='/api')

@app.get('/')
async def hello_world():
    return {
        'mess': 'hello world'
    }

@app.get('/test/a')
async def testA():
    return 'this is a'

@app.get('/test/{id}')
async def test1(id: int):
    return {
        'id': id
    }

# 放这会先匹配到'/test/{id}'
# @app.get('/test/a')
# async def testA():
#     return 'this is a'

# 枚举
class Person(str, Enum):
    name = 'sb'
    age = 12

@app.get('/person/{name}')
async def get_person(name: Person):
    print(name.value, name)
    if name == Person.name:
        return name
    return 'not found'

@app.get('/query')
async def query(a: int = 0, b: int = 1):
    return [a, b]

@app.get('/query_bool/{a}')
async def query_bool(a: str, bool: bool):
    return {
        'a': a,
        'bool': bool
    }

class Animal(BaseModel):
    name: str
    age: int
    color: str = None
    index: int = None

# body
@app.post('/animal')
async def get_animal(animal: Animal):
    return animal

@app.post('/animal_color')
async def get_animal_color(animal: Animal):
    animal_dict = animal.dict()
    animal_dict.update({'color': 'red'})
    return animal_dict

# query
@app.post('/animal_query')
async def animal_query(color: str):
    return {
        'name': 'sb',
        'age': 12,
        'color': color
    }

# body + path
@app.post('/animal/{index}')
async def get_animal_by_index(index: int, animal: Animal):
    animal_dict = animal.dict()
    animal_dict.update({'index': index, 'color': 'red'})
    return animal_dict

# body + path +query
@app.post('/animal_with_query/{index}')
async def get_animal_by_index_and_color(index: int, animal: Animal, color: str):
    animal_dict = animal.dict()
    animal_dict.update({
        'index': index,
        'color': color
    })
    return animal_dict

# Query
@app.get('/test_query')
async def test_query(q: str = Query(None, max_length = 2)):
    res = {
        'a': 1,
        'b': 2
    }
    if q:
        res.update({
            'q': q
        })
    return res

# Query with regex
@app.get('/query_with_regex')
async def query_regex(q: str = Query(None, regex='^abc$')):
    res = {
        'x': 'a',
        'y': 'b'
    }
    if q:
        res.update({
            'q': q
        })
    return res

# Body
@app.post('/test_body')
async def test_body(data = Body(...)):
    return data

# cookie & header
@app.post('/test_cookie_header')
async def test_cookie_and_header(data = Body(...), lan: str = Cookie(None), agent: str = Header(None)):
    return {
        'lan': lan,
        'agent': agent,
        'data': data
    }

# http status
@app.get('/http_status', status_code = status.HTTP_201_CREATED)
async def test_http_status():
    return 'status: 201'

# websocket
@app.websocket_route('/ws')
async def ws(websocket: WebSocket):
    await ws.accept()
    await ws.send_json({
        'msg': 'ws msg'
    })

def test_read_main():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'msg': 'ws msg'
    }

def test_websocket():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = websocket.receive_json()
        assert data == {
            'msg': 'ws msg'
        }

if __name__ == '__main__':
    import uvicorn;
    uvicorn.run(app, host='0.0.0.0', port=8000);
