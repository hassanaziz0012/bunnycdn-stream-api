class AuthorizationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class ServerError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)