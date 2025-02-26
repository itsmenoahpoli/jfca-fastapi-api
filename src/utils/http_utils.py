from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def HTTPResponse(status_code: status, detail: dict | str):
	return JSONResponse(
		status_code=status_code,
		content=jsonable_encoder(detail)
	)