__author__ = '4423'
import hashlib
import lib.Settings
import lib.User

class Manager:

    @staticmethod
    def hash_password(user_name, password):
        """Hash the users password

        Parameters
        ----------
        user_name : string
        password : string

        Returns
        -------
        string
        """
        return hashlib.sha256(user_name + lib.Settings.GLOBAL_SALT + password).hexdigest()
