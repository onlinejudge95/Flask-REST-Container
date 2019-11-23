class BaseError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class UserExistsError(BaseError):
    pass


class UserDoesNotExistsError(BaseError):
    pass


class ForbiddenOperationError(BaseError):
    pass


class IllegalArgumentError(BaseError):
    pass
