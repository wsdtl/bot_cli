from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def FastAPIAllowed(app: "FastAPI") -> None:
    """
    FastAPI 允许跨域请求
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
