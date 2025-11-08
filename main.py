from fastapi import FastAPI

app = FastAPI(
    title="TFM API",
    description="API del TFM",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Hola, esta es la API de mi TFM"}