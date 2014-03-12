__author__ = '4423'


class Log:
    """Log class for debugging"""
    
    DISABLED = 200
    CRITICAL = 100
    IMPORTANT = 50
    NOTICE = 10
    

    level = Log.Disabled

    @staticmethod
    def add(log_text, level=Log.NOTICE):
        """Add a log entry

        Parameters
        ----------
        log_text : string
        """
        if Log.level <= level:
            print "Log(%d): %s" % (level, log_text)

    @staticmethod
    def enable_log(level=CRITICAL):
        """Enable the log

        Parameters
        ----------
        enable : Boolean
        """
        Log._level = level
