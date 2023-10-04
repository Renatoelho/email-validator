#!/home/user01/.virtualenvs/bin/python3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models.payload import Payload
from models.response import Response
from models.errors import Errors


app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    try:
        return JSONResponse(status_code=200, content={"status": "everything is OK"})
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
    response_model=Response,
    responses={
        200: {"model": Response},
        500: {"model": Errors}
        
    }
)
async def email_validator(payload: Payload):
    try:
        data_payload =  Payload(**payload)
        data_payload = data_payload.dict()
        return JSONResponse(
            status_code=200,
            content=data_payload
        )
    except Exception as erro:
        erro = f"The following error occurred on the server: {erro}"
        content_error = (
            {
                "status": "",
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
