import os
import requests
import logging
import app.ayo_nlu_protection as ayo_nlu_protection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from fastapi.responses import JSONResponse

app = FastAPI()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)


class BaseInput(BaseModel):
    user_id: str
    user_name: str


class ProtectionInput(BaseInput):
    session: str
    action: str
    config: Optional[Any] = None


@app.post("/variables")
async def protection_variables(variables_input: BaseInput):
    try:
        user_id = variables_input.user_id
        user_name = variables_input.user_name

        logger.info("Received post request at /variables:")
        logger.info("user_id: %s", user_id)
        logger.info("user_name: %s", user_name)

        response = ayo_nlu_protection.patch_user_variables(user_id, user_name)
        logger.info("response: %s", response)
        # return JSONResponse(content={"message": "Patch request successful"})
        # return JSONResponse(content={"message": response})


    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/interact")
async def protection_interact(interact_input: ProtectionInput):
    try:
        user_id = interact_input.user_id
        user_name = interact_input.user_name
        session = interact_input.session
        request = interact_input.action
        DMconfig = interact_input.config

        logger.info("Received post request at /interact:")
        logger.info("user_id: %s", user_id)
        logger.info("user_name: %s", user_name)
        logger.info("session: %s", session)
        logger.info("user_enquiry: %s", request)
        logger.info("DMconfig: %s", DMconfig)

        # response = ayo_nlu_protection.post_user_enquiry(DMconfig, session, user_id, request)
        response = ayo_nlu_protection.analyze_text(request)
        logger.info("response: %s", response)
        # response = ayo_nlu_protection.anonymize_text(request,response)
        # logger.info("response: %s", response)

        # return JSONResponse(content={"message": "Post request successful"})
        # return JSONResponse(content={"message": response})


    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")



