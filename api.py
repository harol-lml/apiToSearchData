from typing import Union
from fastapi import FastAPI
from get_data import get_data

app = FastAPI()

@app.get("/datascr")
def read_item(id: Union[str, None] = None, per: Union[str, None] = None, pages: Union[str, None] = 1):
    if id and per:
        data = get_data.getById(id, per, 1)
        if 'error' in data : return data
        if pages <= 1: return data
        for index, number in enumerate(range(2, pages), start=2):
            print(f'Número {index}: {number}')
            dt = get_data.getById(id, per, number)
            if len(dt) == 0:
                break
            data.extend(dt)
        return data
    return 'No data'

@app.get("/datam")
def read_data(id: Union[str, None] = None, per: Union[str, None] = None):
    if id and per:
        data = get_data.getDataInMongo(id, per)
        return data
    return {'error':'no data'}