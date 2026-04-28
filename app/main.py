from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
try:
	from .api.merge import router as merge_router
except Exception:
	merge_router = None

if merge_router:
	app.include_router(merge_router)
try:
    from .api.compress_pdf import router as compress_router
except Exception:
    compress_router = None

if compress_router:
    app.include_router(compress_router)


@app.get("/")
async def root():
	return {"message": "Welcome to the PDF Merger API. Use the /merge endpoint to merge PDF files."}



if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)