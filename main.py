from fastapi import FastAPI 
# import config
from api.API_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
import config

app = FastAPI(
     title='FastAPI-Customize template',
    #  description= config.app_description,
     version="1.0.0",

)
# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
#     allow_origins=["http://localhost:8080"],  # Allow requests from the frontend's origin
    allow_origins=config.origins,
    allow_credentials=True,  # Allow cookies to be sent along with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get('/')
def start_up():
     return ({'I AM':'Alive'})
#test
app.include_router(api_router,prefix='/api')