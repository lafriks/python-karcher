# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

class KarcherHomeException(Exception):
    """Exception raised for errors in the Karcher Home Robots library.

    Attributes:
        code -- error code
        message -- explanation of the error
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)


class KarcherHomeAccessDenied(KarcherHomeException):
    """Exception raised when user has no access for resource.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(608, self.message)


class KarcherHomeInvalidAuth(KarcherHomeException):
    """Exception raised when wrong credentials are provided."""

    def __init__(self):
        super().__init__(620, 'The username or password is incorrect')


class KarcherHomeTokenExpired(KarcherHomeException):
    """Exception raised when token has been expired."""

    def __init__(self):
        super().__init__(609,
                         'Unauthorized or authorization expired, please log in again')


def handle_error_code(code, message):
    if code == 608:
        raise KarcherHomeAccessDenied('Forbidden')
    elif code == 609:
        raise KarcherHomeTokenExpired()
    elif code == 613:
        raise KarcherHomeException(613, 'Invalid token')
    elif code == 620:
        raise KarcherHomeInvalidAuth()
    else:
        raise KarcherHomeException(code, message)
