from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.routes.analyze import router as analyze_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.security import require_api_key

configure_logging()
sentry_sdk.init(dsn=None, traces_sample_rate=0.0)

app = FastAPI(title=settings.app_name)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

origins = [x.strip() for x in settings.allow_cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router, dependencies=[Depends(require_api_key)])
app.include_router(chat_router, dependencies=[Depends(require_api_key)])

Instrumentator().instrument(app).expose(app)
