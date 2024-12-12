from fastapi import FastAPI 
# import config
from api.API_v1.api import api_router


app = FastAPI(
     title='FastAPI-Customize template',
    #  description= config.app_description,
     version="1.0.0",

)

@app.get('/')
def start_up():
     return ({'I AM':'Alive'})
#test
app.include_router(api_router,prefix='/api')