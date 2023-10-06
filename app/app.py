#!/home/user01/.virtualenvs/bin/python3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models.payload import Payload
from models.result import Result
from models.health import Health
from models.errors import Errors

from utils.dns_domain import run_dns_record


app = FastAPI()

@app.get("/docs", include_in_schema=False)
async def custom_redoc():
    return redoc.html()


@app.get("/healthcheck",
    response_model=Health,
    responses={200: {"model": Health}, 500: {"model": Errors}}
)
async def healthcheck():
    try:
        content = {"status": True, "mensage": "everything is OK"}
        return JSONResponse(status_code=200, content=content)
    except Exception as erro:
        erro = f"The following error occurred on the server: {erro}"
        content_error = (
            {
                "status": "",
                "erro": erro 
            }
        )
        return JSONResponse(status_code=500, content=content_error)


@app.post(
    "/email-validator",
    response_model=Result,
    responses={200: {"model": Result}, 500: {"model": Errors}}
)
async def email_validator(payload: Payload):
    try:
        return JSONResponse(status_code=200, content=run_dns_record(payload.email))
    except Exception as erro:
        erro = f"The following error occurred on the server: {erro}"
        content_error = (
            {
                "status": False,
                "erro": erro 
            }
        )
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
