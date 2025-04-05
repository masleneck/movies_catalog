from app.create_app import create_app

app = create_app()

# uvicorn app.main:app --reload