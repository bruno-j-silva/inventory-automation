import re
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException

from app.core.config import Settings
from app.core.database import DatabaseProbe, PostgresProbe
from app.core.logging import configure_logging


def error_response(request: Request, status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": [],
                "request_id": request.state.request_id,
            }
        },
    )


def create_app(settings: Settings | None = None, database: DatabaseProbe | None = None) -> FastAPI:
    configuration = settings or Settings()
    probe = database or PostgresProbe(configuration)
    logger = configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            probe.close()

    app = FastAPI(
        title="Gestão e Inventário de Automações",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/api/docs" if configuration.environment != "production" else None,
        redoc_url=None,
        openapi_url="/api/openapi.json" if configuration.environment != "production" else None,
    )

    @app.middleware("http")
    async def request_context(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        supplied = request.headers.get("X-Request-ID", "")
        request.state.request_id = (
            supplied if re.fullmatch(r"[A-Za-z0-9_-]{1,64}", supplied) else str(uuid4())
        )
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            response = error_response(request, 500, "INTERNAL_ERROR", "Erro interno do serviço.")
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        route = request.scope.get("route")
        logger.info(
            "http_request",
            extra={
                "request_id": request.state.request_id,
                "method": request.method,
                "route": getattr(route, "path", "unmatched"),
                "status": response.status_code,
                "duration_ms": round((perf_counter() - started) * 1000, 2),
            },
        )
        return response

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
        return error_response(
            request,
            exc.status_code,
            "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR",
            "Recurso não encontrado." if exc.status_code == 404 else "Requisição recusada.",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(request, 422, "VALIDATION_ERROR", "Dados de entrada inválidos.")

    @app.get("/api/health/live", tags=["health"])
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/health/ready", tags=["health"], response_model=None)
    def ready(request: Request) -> dict[str, str] | JSONResponse:
        if not probe.ready():
            return error_response(request, 503, "SERVICE_UNAVAILABLE", "Serviço indisponível.")
        return {"status": "ready"}

    return app
