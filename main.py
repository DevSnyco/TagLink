import os
import uvicorn

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, Response
from fastapi.responses import JSONResponse

load_dotenv(find_dotenv())
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins = [],
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)
app.card_content = {}

@app.get("/")
async def read_root():
	return "OK"

@app.post("/update")
async def update_card(request: Request):
	data = await request.json()
	if request.headers.get("Authorization") != os.getenv("AUTH_KEY"):
		return JSONResponse(content = {"status": "unauthorized"})

	if app.card_content.get(f"{data.get("card_id")}") == data.get("content"):
		return JSONResponse(content = {"status": "no changes"})

	app.card_content[f"{data.get("card_id")}"] = data.get("content")
	return JSONResponse(content = {"status": "updated"})

@app.get("/{card_id}")
async def get_card(card_id: str):
	content = app.card_content.get(f"{card_id}")
	if content is None:
		return JSONResponse(content = {"status": "not found"})
	if content.startswith("http://") or content.startswith("https://"):
		return RedirectResponse(content)
	return Response(content = content, media_type = "text/plain")

if __name__ == "__main__":
	uvicorn.run(app, host = "127.0.0.1", port = 8009)