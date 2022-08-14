from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn
from pydantic import BaseModel
app = FastAPI()

inventory = {}


class Item(BaseModel):
    name: str
    price: float
    # means field is optional
    brand: str = None


class UpdateItem(BaseModel):
    name: str = None
    price: float = None
    brand: str = None


# basic get request
@app.get('/')
def home():
    return {"Data": "Returned Data"}


# get request with passed argument
@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail='item not found')
    return inventory[item_id]


# get request with passed argument along with description to clarify. Also set that input is Greater Than 0
@app.get("/get-item-with-description/{item_id}")
def get_item_with_description(item_id: int = Path(description='Enter product ID here to get more info'), gt=0):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail='item not found')
    return inventory[item_id]


# get request with query
# http://127.0.0.1:5000/get-by-name?name=Milk
# name:st = None means the parameter isn't required for query to complete
# http://127.0.0.1:8000/get-by-name?test=1&name=Milk
@app.get('/get-by-name')
def get_by_name(*, name: str = None, test: int):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        raise HTTPException(status_code=404, detail='item not found')


@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=404, detail='item not found')
    inventory[item_id] = item
    return inventory[item_id]


@app.patch('/update-item')
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail='item not found')
    if item.name is not None:
        inventory[item_id].name = item.name
    if item.price is not None:
        inventory[item_id].price = item.price
    if item.brand is not None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


@app.delete('/delete-item')
def delete_item(item_id: int = Query(..., description='the id does not exist', gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail='item not found')
    del inventory[item_id]
    return {'Success': 'Item was deleted successfully'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, loop="auto")

