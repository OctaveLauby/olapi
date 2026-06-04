class AuthenticationError(Exception):
    pass


class UserExistsError(AuthenticationError):
    pass


class UnauthorizedError(AuthenticationError):
    pass
