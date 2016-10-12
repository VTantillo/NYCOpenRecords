"""
 .. module: utils

"""

from base64 import b64decode

class InvalidUserException(Exception):

    def __init__(self, user):
        """
        :param user: the current_user as define in flask_login
        """
        super(InvalidUserException, self).__init__(
            "Invalid user: {}".format(user))


def b64decode_lenient(data):
    """
    Decodes base64 (bytes or str), padding being optional

    :param data: a string or bytes-like object of base64 data
    :return: a decoded string
    """
    if type(data) is str:
        data = data.encode()
    data += b'=' * (4 - (len(data) % 4))
    return b64decode(data).decode()
