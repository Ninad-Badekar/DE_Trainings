from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class UserData(BaseModel):
    name: str
    email: str
    message: str

@app.post("/submit/")
def submit_data(user: UserData):
    summary = {
        "message": f"Hello {user.name}, we received your message!",
        "email": user.email,
        "submitted_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return summary
