"""Random Utilities

Function from this class are generic enough that I don't know where else to put them

"""

import hashlib
import random
import string



## TODO put this in config
# from config import PASSWORD_SALT_LENGTH
PASSWORD_SALT_LENGTH = 16

class Util(object):

    @classmethod
    def get_file_checksum(cls, path_to_file):
        """

        """

        sha256 = hashlib.sha256()

        with open(path_to_file, 'rb') as f:

## digest block size is 64 bytes, use any multiple for read length
## '' is a sentinel for EOF. iter stops when sentinel is returned
## by the lambda function
            for block in iter(lambda: f.read(8192), ''):

                sha256.update(block)

        return sha256.hexdigest()


    @classmethod
    def get_checksum(cls, string_):
        """

        """

        sha256 = hashlib.sha256()

        sha256.update(string_)

        return sha256.hexdigest()

## TODO: replace all password stuff with passlib
    # @classmethod
    # def get_password_hash(cls, password, salt):
    #     """

    #     """

    #     return cls.get_checksum(salt + password)

    # @classmethod
    # def verify_password(cls, password, salt, password_hash):
    #     """

    #     """

    #     return password_hash == cls.get_password_hash(password, salt)

    # @classmethod
    # def get_password_salt(cls):
    #     """

    #     """

    #     return ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(PASSWORD_SALT_LENGTH))


    @classmethod
    def all_subclasses(cls, base_class):
        """

        """

        return base_class.__subclasses__() + [g for s in base_class.__subclasses__() for g in cls.all_subclasses(s)]


