class ServerError(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class ObjectNotFound(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class InvalidInputData(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class ObjectNotUpdated(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class ObjectNotCreated(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class ObjectNotDeleted(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class ObjectAlreadyExists(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class PermissionDenied(BaseException):
    def __init__(self) -> None:
        super().__init__()


class InvalidRequestData(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail


class InvalidResponse(BaseException):
    def __init__(self, detail: str) -> None:
        super().__init__()
        self.detail = detail
