__author__ = '4423'


class UpdateManager(object):
    """Mange the updating of data objects to stop needless MySQL Queries"""

    _to_update = {}

    def __init__(self):
        pass

    def needs_updating(self):
        """Check if the Object needs updating

        Returns
        -------
        Boolean
        """
        return True if self._to_update else False

    def _add_update_field(self, db_field, class_var):
        """Add a field to the update dictionary

        Parameters
        ----------
        db_field : string
        class_var : string
        """
        self._to_update[db_field] = class_var

    def _create_update_string(self):
        """Create the SQL update string

        Returns
        -------
        string
        """
        out = ""

        for field in self._to_update:
            out += " `%s` = %%s," % field

        return out[:-1]

    def _create_update_var_list(self):
        """Create a list of vars to pass to the SQL update

        Returns
        -------
        list
        """
        out = []

        for field in self._to_update:
            out.append(getattr(self, self._to_update[field]))

        return out