import uvicorn
from fastapi import FastAPI


from launch import (
    lifespan,
    FastAPIAllowed,
    LOGGING_CONFIG,
    FastAPILoadRouter,
)


def create_app():
    # 创建 FasatAPI 实例
    app = FastAPI(lifespan=lifespan)

    # FasatAPI 跨域设置
    FastAPIAllowed(app)

    # 导入模块设置
    FastAPILoadRouter()

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=LOGGING_CONFIG,
    )
