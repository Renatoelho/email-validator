#!/home/user_email/.virtualenvs/bin/python3

from models.payload import Payload
from models.result import Result
from models.health import Health
from models.errors import Errors

from utils.dns_domain import run_dns_record
from utils.domains import content_error_response

from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get(
    "/healthcheck",
    response_model=Health,
    responses={200: {"model": Health}, 500: {"model": Errors}}
)
async def healthcheck():
    try:
        content = {"status": True, "mensage": "everything is OK"}
        return JSONResponse(status_code=200, content=content)
    except Exception as erro:
        erro = f"The following error occurred on the server: {erro}"
        content_error = content_error_response(erro)
        return JSONResponse(status_code=500, content=content_error)


@app.post(
    "/email-validator",
    response_model=Result,
    responses={200: {"model": Result}, 500: {"model": Errors}}
)
async def email_validator(payload: Payload):
    try:
        content_resul = Result(**run_dns_record(payload.email)).json()
        return JSONResponse(status_code=200, content=content_resul)
    except Exception as erro:
        erro = f"The following error occurred on the server: {erro}"
        content_error = content_error_response(erro)
        return JSONResponse(status_code=500, content=content_error)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=8888,
        log_level="info",
        reload=True
    )
