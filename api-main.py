from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
import time
import logging

from app.api.router import api_router
from core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API...")

    # Inicialização:
    # - banco
    # - clientes de IA
    # - Redis
    # - conexões externas

    yield

    logger.info("Shutting down API...")

    # Encerramento:
    # - fechar conexões
    # - liberar recursos

app = FastAPI(
    title="API-IA",
    version="1.0.0",
    description="API para integração com servidores de Inteligência Artificial",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else False,
    redoc_url="/redoc" if settings.DEBUG else False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


# =========================================================
# REQUEST ID + TEMPO DE EXECUÇÃO
# =========================================================

class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid4())
        )

        start = time.perf_counter()

        try:
            response = await call_next(request)

        except Exception:
            logger.exception(
                "Unhandled exception | request_id=%s",
                request_id
            )

            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                },
            )

        duration = time.perf_counter() - start

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "%s %s | status=%s | %.3fs | request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration,
            request_id,
        )

        return response


app.add_middleware(RequestMiddleware)


# =========================================================
# ROTAS
# =========================================================

app.include_router(
    api_router,
    prefix="/api/v1"
)

@app.get("/health")
async def health():
    return {"status": "ok"}

