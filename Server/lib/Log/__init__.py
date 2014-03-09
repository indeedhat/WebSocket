__author__ = '4423'


class Log:
    """Log class for debugging"""

    enabled = False

    @staticmethod
    def add(log_text):
        """Add a log entry

        Parameters
        ----------
        log_text : string
        """
        if Log.enabled:
            print log_text

    @staticmethod
    def enable_log(enable=True):
        """Enable the log

        Parameters
        ----------
        enable : Boolean
        """
        Log.enabled = enable