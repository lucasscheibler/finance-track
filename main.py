from app import app
import uvicorn


application = app.create_app()

if __name__ == "__main__":
    uvicorn.run(application, host="127.0.0.1", port=8000)