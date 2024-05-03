from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .routers.jira import router as jira_router
from .routers.limiter import limiter
from .routers.user import router as user_router

app = FastAPI()

app.include_router(jira_router)
app.include_router(user_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



