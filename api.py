from typing import Union
from fastapi import FastAPI
from get_data import get_data

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data")
def read_item(id: Union[str, None] = None, per: Union[str, None] = None):
    if id and per:
        data = get_data.getById(id, per, 1)
        if 'error' in data : return data
        for index, number in enumerate(range(2, 29), start=2):
            print(f'Número {index}: {number}')
            dt = get_data.getById(id, per, number)
            if len(dt) == 0:
                break
            data.extend(dt)
        return data
    return 'No data'