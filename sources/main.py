from fastapi import FastAPI

from sources.views import user_view


def create_application() -> FastAPI:
    test_task_web_application = FastAPI(
        title='Test task application',
        version='1.0',
    )
    test_task_web_application.include_router(user_view)
    return test_task_web_application


application = create_application()
