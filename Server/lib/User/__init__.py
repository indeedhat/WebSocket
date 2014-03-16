__author__ = '4423'
from lib.User.Manager import Manager
from lib.DB.UpdateManager import UpdateManager
from lib.DB.MySQL import MySQL


class User(UpdateManager):

    SELECT_SQL = """
      user_id as _user_id,
      user_name as _user_name,
      user_email as _user_email,
      register_date as _register_date
    """

    _user_id = 0
    _user_name = ""
    _user_email = ""
    _register_date = 0
    _user_password = ""

    def get_user_id(self):
        """Getter for user_id attribute

        Returns
        -------
        int
        """
        return self._user_id

    def get_user_name(self):
        """Getter for user_name attribute

        Returns
        -------
        string
        """
        return self._user_name

    def get_user_email(self):
        """Getter for user_email attribute

        Returns
        -------
        string
        """
        return self._user_email

    def get_register_date(self):
        """Getter for register_date attribute

        Returns
        -------
        int
        """
        return self._register_date

    def set_user_name(self, user_name):
        """Setter for the user_name attribute

        Parameters
        ----------
        user_name : string

        Returns
        -------
        self
        """
        if self._user_name != user_name:
            self._user_name = user_name
            self._add_update_field('user_name', '_user_name')

        return self

    def set_user_email(self, user_email):
        """Setter for the user_email attribute

        Parameters
        ----------
        user_email : string

        Returns
        -------
        self
        """
        if self._user_email != user_email:
            self._user_email = user_email
            self._add_update_field('user_email', '_user_email')

        return self

    def set_user_password(self, password):
        """Setter for the user_password attribute
        (Setter only, no getter)

        Parameters
        ----------
        user_password : string

        Returns
        -------
        self
        """
        self._user_password = Manager.hash_password(self._user_name, password)
        self._add_update_field('user_password', '_user_password')

        return self

    def save(self):
        """Update the database if required"""
        if self.needs_updating():
            MySQL.get().query("""
              UPDATE
                users
              SET
                %s
              WHERE
                user_id = %s
            """ % (self._create_update_string(), self._user_id)
            , self._create_update_var_list())