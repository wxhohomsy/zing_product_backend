from zing_product_backend.core.common import ErrorMessages


class PredefinedException(Exception):
    def __init__(self, message: ErrorMessages, detail: str, code):
        self.message = message
        self.code = code
        self.detail = detail


class NotFoundError(PredefinedException):
    def __init__(self, detail: str = None):
        super().__init__(message=ErrorMessages.DATA_NOT_FOUND, detail=detail, code=400)


class OutDatedDataError(PredefinedException):
    def __init__(self, detail: str = None):
        super().__init__(message=ErrorMessages.DATA_NOT_FOUND, detail=detail, code=400)


class NotImplementError(PredefinedException):
    def __init__(self, detail: str = None):
        super().__init__(message=ErrorMessages.DATA_NOT_FOUND, detail=detail, code=400)


class DuplicateError(PredefinedException):
    def __init__(self, detail: str = None):
        super().__init__(message=ErrorMessages.DUPLICATE_DATA, detail=detail, code=400)


class InsufficientPrivilegeError(PredefinedException):
    def __init__(self, detail: str = None):
        super().__init__(message=ErrorMessages.INSUFFICIENT_PRIVILEGE, detail=detail, code=403)