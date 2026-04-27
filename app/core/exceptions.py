from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, detail=message)


class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=400, detail=message)


class ForbiddenException(HTTPException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=403, detail=message)