from fastapi import FastAPI
from database import init_db
from routers import department, employee

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(department.router)
app.include_router(employee.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
