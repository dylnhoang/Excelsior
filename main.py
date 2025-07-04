from fastapi import FastAPI
from routers import upload, formula, action, download, status, data, export

app = FastAPI()
app.include_router(upload.router)
app.include_router(formula.router)
app.include_router(action.router)
app.include_router(download.router)
app.include_router(status.router)
app.include_router(data.router)
app.include_router(export.router)
app.include_router(data.router, tags=["preview"])