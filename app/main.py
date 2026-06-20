from fastapi import FastAPI
from app.api.routers.auth.sign_in import router as auth_router
from app.api.routers.auth.sign_up import router as sign_up_router
from app.api.routers.auth.google_auth import router as google_auth_router
from app.api.routes.users import router as users_router
from app.api.routes.events import router as events_router
from app.api.routes.expenses import router as expenses_router
from app.api.routes.members import router as members_router
from app.api.routes.splits import router as splits_router
from app.api.routes.balances import router as balances_router
from app.api.routes.settlements import router as settlements_router

app = FastAPI(
    title="Expense Tracker",
    version="0.1.0",
    openapi_url="/openapi.json"
)

app.include_router(auth_router)
app.include_router(sign_up_router)
app.include_router(google_auth_router)
app.include_router(users_router)
app.include_router(events_router)
app.include_router(expenses_router)
app.include_router(members_router)
app.include_router(splits_router)
app.include_router(balances_router)
app.include_router(settlements_router)
