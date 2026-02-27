"""Error handling middleware for the chatbot feature."""

import traceback
from typing import Callable, Awaitable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from exceptions.chat import ChatException


async def chat_error_handler(request: Request, call_next: Callable[[Request], Awaitable]):
    """
    Middleware to handle chat-specific errors globally.

    Args:
        request: The incoming request
        call_next: The next middleware in the chain

    Returns:
        Response from the next middleware or error response
    """
    try:
        response = await call_next(request)
        return response
    except ChatException as e:
        # Handle custom chat exceptions
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "type": "chat_error",
                    "code": e.error_code,
                    "message": e.message
                }
            }
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the full error for debugging (in a real implementation)
        print(f"Unexpected error in chat endpoint: {str(e)}")
        print(traceback.format_exc())

        # Return a generic error response
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "internal_server_error",
                    "code": "INTERNAL_ERROR",
                    "message": "An internal server error occurred"
                }
            }
        )


def add_chat_error_handlers(app):
    """
    Add error handlers to the FastAPI app.

    Args:
        app: The FastAPI application instance
    """
    # Add the middleware
    app.middleware("http")(chat_error_handler)

    # Add specific exception handlers
    @app.exception_handler(ChatException)
    async def handle_chat_exception(request: Request, exc: ChatException):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "type": "chat_error",
                    "code": exc.error_code,
                    "message": exc.message
                }
            }
        )

    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        # Log the error (in a real implementation)
        print(f"General error: {str(exc)}")
        print(traceback.format_exc())

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "internal_server_error",
                    "code": "INTERNAL_ERROR",
                    "message": "An internal server error occurred"
                }
            }
        )
