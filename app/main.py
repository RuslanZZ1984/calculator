from fastapi import FastAPI
from app.api.routes import users, events, expenses

app = FastAPI(title="Expense Tracker")

app.include_router(users.router)
app.include_router(events.router)
app.include_router(expenses.router)

# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(events.router, prefix="/events", tags=["Events"])
# app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])