class BaseError(Exception):
    def __init__(self, message):
        Exception.__init__(self)

        self.response = {"status": "fail", "message": message}

    def to_json(self):
        return self.response


class UserExistsError(BaseError):
    def __init__(self, email, message):
        BaseError.__init__(self, message)
        self.email = email

    def to_json(self):
        self.response["message"] = self.response["message"].format(self.email)
        return self.response


class UserDoesNotExistsError(BaseError):
    def __init__(self, public_id, message):
        BaseError.__init__(self, message)
        self.public_id = public_id

    def to_json(self):
        self.response["message"] = self.response["message"].format(
            self.public_id
        )
        return self.response


class ForbiddenOperationError(BaseError):
    def __init__(self, message):
        BaseError.__init__(self, message)


class IllegalArgumentError(BaseError):
    def __init__(self, message):
        BaseError.__init__(self, message)
