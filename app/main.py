import os
import requests
import logging
import app.ayo_nlu_protection as ayo_nlu_protection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse



AYO_WHATSAPP_API = os.environ.get('AYO_WHATSAPP_API')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID')
VF_DM_URL = os.environ.get('VF_DM_URL')
VF_API_KEY = os.environ.get('VF_API_KEY')

app = FastAPI()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)


class BaseInput(BaseModel):
    user_id: str
    user_name: str


class ProtectionInput(BaseInput):
    session: str
    action: str
    config: Optional[str] = None


@app.post("/variables")
async def protection_variables(variables_input: BaseInput):
    try:
        user_id = variables_input.user_id
        user_name = variables_input.user_name
        
        logger.info("Received post request:")
        logger.info("user_id: %s", user_id)
        logger.info("user_name: %s", user_name)

        response = ayo_nlu_protection.patch_user_variables(VF_DM_URL, user_id, user_name, VF_API_KEY)
        return JSONResponse(content={"message": "Patch request successful"})
        return JSONResponse(content={"message": response})


    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/interact")
async def protection_interact(interact_input: ProtectionInput):
    try:
        user_id = interact_input.user_id
        session = interact_input.session
        request = interact_input.request
        DMconfig = interact_input.DMconfig

        logger.info("Received scheduler get request:")
        logger.info("user_id: %s", user_id)
        logger.info("session: %s", session)
        logger.info("user_enquiry: %s", request)
        logger.info("DMconfig: %s", DMconfig)

        response = ayo_nlu_protection.post_user_enquiry(DMconfig, session, user_id, request)
        return JSONResponse(content={"message": "Post request successful"})
        return JSONResponse(content={"message": response})


    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")



