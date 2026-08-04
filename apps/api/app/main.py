from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import activity_router, auth_router, comments_router, notifications_router, projects_router, scripts_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(projects_router.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(scripts_router.router, prefix="/api/v1", tags=["scripts"])
app.include_router(comments_router.router, prefix="/api/v1", tags=["comments"])
app.include_router(notifications_router.router, prefix="/api/v1", tags=["notifications"])
app.include_router(activity_router.router, prefix="/api/v1", tags=["activity"])
# Further routers are registered here as each module is built:
# app.include_router(export_router.router, prefix="/api/v1", tags=["export"])


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
