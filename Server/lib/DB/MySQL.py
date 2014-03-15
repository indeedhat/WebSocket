__author__ = '4423'

import lib.Settings.DB.MySQL as DBS
import MySQLdb
from MySQLdb.cursors import DictCursor

class MySQL:
    _instances = {}  # static

    _conn = ""
    _host = ""
    _dbase = ""
    _user = ""
    _passwd = ""

    @staticmethod
    def get(connection = "master", host = None, dbase = None, user = None, passwd = None):
        """Return an instance of the MySQL Object

        Parameters
        ----------
        connection : String
        host : String
        dbase : String
        user : String
        passwd : String

        Returns
        -------
        lib.DB.MySQL.MySQL
        """
        if connection in MySQL._instances:
            return MySQL._instances[connection]

        MySQL._instances[connection] = MySQL(host = host, dbbase = dbase, user = user, passwd = passwd)
        return MySQL._instances[connection]

    def __init__(self, host = None, dbase = None, user = None, passwd = None):
        """Create instance of MySQL Object

        Parameters
        ----------
        host : String
        dbase : String
        user : String
        passwd : String
        """
        self._host   = host   if host   else DBS.HOST
        self._dbase  = dbase  if dbase  else DBS.DBNAME
        self._user   = user   if user   else DBS.USER
        self._passwd = passwd if passwd else DBS.PASS

    def _connect(self):
        """Astablish the connection to the database"""
        if self._conn is None:
            self._conn = MySQLdb.connect(
                host   = self._host,
                db     = self._dbase,
                user   = self._user,
                passwd = self._passwd,
                cursorclass = DictCursor
            )

    def query(self, query, args):
        """Perform a query

        Parameters
        ----------
        query : String
        args : list|tuple
        """
        # connect and create cursor
        self._connect()
        cur = self._conn.cursor()

        # run query
        if isinstance(args, (tuple, list)) and isinstance(args[0], (tuple, list)):
            cur.executemany(query, args)  # multiple rows
        else:
            cur.execute(query, args)  # single row

        # commit changes to the server
        cur.commit()

    def quick_result(self, query, args):
        """Return the first field of the first row of the query

        Parameters
        ----------
        query : String
        args : list|tuple

        Returns
        -------
        mixed
        """
        self._connect()
        cur = self._conn.cursor()

        res = cur.fetchone(query, args)
        return res[0] if 0 in res else None

    def query_fetch(self, query, args):
        """Return a single row from the database

        Parameters
        ----------
        query : String
        args : list|tuple

        Returns
        -------
        dictionary
        """
        self._connect()
        cur = self._conn.cursor()

        return cur.fetchone(query, args)

    def query_fetch_all(self, query, args):
        """Return multiple rows from the database

        Parameters
        ----------
        query : String
        args : list|tuple

        Returns
        -------
        tuple
        """
        self._connect()
        cur = self._conn.cursor()

        return cur.fetchmany(query, args)

    def query_fetch_object(self, query, args, class_location):
        """Return a single row from the database as an object

        Parameters
        ----------
        query : String
        args : list|tuple

        Returns
        -------
        dictionary
        """
        self._connect()
        cur = self._conn.cursor()

        res = cur.fetchone(query, args)

        components = class_location.rsplit('.', 1)

        return self._fetch_object(
            getattr(components[0], components[1]),
            res
        )

    def query_fetch_objects(self, query, args, class_location):
        """Return multiple rows from the database as objects

        Parameters
        ----------
        query : String
        args : list|tuple

        Returns
        -------
        list
        """
        self._connect()
        cur = self._conn.cursor()

        res = cur.fetchmany(query, args)

        components = class_location.rsplit('.', 1)

        out = []
        for row in res:
            out.append(
                self._fetch_object(
                    getattr(components[0], components[1]),
                    row
                )
            )

        return out

    @staticmethod
    def _fetch_object(instance, results):
        """Assign results to the object

        Parameters
        ----------
        instance : {object instance}
        results : dictionary

        Returns
        -------
        {object instance}
        """
        for var in results:
            setattr(instance, var, results[var])

        return instance