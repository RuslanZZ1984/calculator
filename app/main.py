from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.routers.auth.sign_in import router as auth_router
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
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,
    }
)

# Настройка авторизации для Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Добавляем поддержку cookie и bearer авторизации
    openapi_schema["components"]["securitySchemes"] = {
        "CookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
            "description": "Cookie-based authentication"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Подключение роутеров
app.include_router(auth_router)
app.include_router(google_auth_router)
app.include_router(users_router)
app.include_router(events_router)
app.include_router(expenses_router)
app.include_router(members_router)
app.include_router(splits_router)
app.include_router(balances_router)
app.include_router(settlements_router)

print("\n=== Registered routes ===")
for route in app.routes:
    if hasattr(route, "methods"):
        print(f"  {route.methods} {route.path}")
print("========================\n")
