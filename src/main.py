import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from api.v1 import webhook_view, bot_view
from core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/gitlab-gateway/api/openapi",
    openapi_url="/gitlab-gateway/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


app.include_router(webhook_view.router, prefix="/api/v1/webhook", tags=["gitlab"])
app.include_router(bot_view.router, prefix="/api/v1/bot", tags=["gitlab"])


if __name__ == "__main__":
    uvicorn.run("main:app", port=8050, host="localhost", reload=True)
