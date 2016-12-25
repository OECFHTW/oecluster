#! /usr/bin/python3

# Author: nico

__version__ = "1.0"

import logging

# Format definition:
logging.basicConfig(format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)


class Log(object):
    """This class prints logging information for the specified class.

    Depending on the information level the log is printed to the stdout stream.
    The best way to create a logger is to initialize an object within the init method:

    def __init__(self, ...)
        self._logger = Log.get_logger(self.__class__.__name__)

    In your functions you may use the logger, e.g.:

    def my_little_big_planet(self, planet="Nico's Planet!!!")
        self._logger.info("received list from %s", planet[0])


    You may also call it without initialization:
    def my_cool_function(self):
        Log.info(self, "This is a cool log.info from %s", 'my function!!')
    """
    @staticmethod
    def get_logger(name=None, obj=None):
        """Returns a logger object

        :param name: the name of the calling class/function
        :param obj: self-object of the calling class/function
        :return: a Logger object for the calling object
        """
        if name:
            return logging.getLogger(name)
        elif obj:
            return logging.getLogger(obj.__class__.__name__)

    @staticmethod
    def debug(obj, *args):
        """Prints debug messages

        :param obj: the object/string to log
        :param args: the arguments to set within the string - works like c-style printf %s/%d/...
        :return: None
        """
        Log.get_logger(obj=obj)
        if len(args) > 1:
            logging.debug(args[0], args[1:])
        else:
            logging.debug(args[0])

    @staticmethod
    def warning(obj, *args):
        """Prints warning messages

        :param obj: the object/string to log
        :param args: the arguments to set within the string - works like c-style printf %s/%d/...
        :return: None
        """
        logger = Log.get_logger(obj=obj)
        if len(args) > 1:
            logger.warning(args[0], args[1:])
        else:
            logger.warning(args[0])

    @staticmethod
    def info(obj, *args):
        """Prints info messages

        :param obj: the object/string to log
        :param args: the arguments to set within the string - works like c-style printf %s/%d/...
        :return: None
        """
        logger = Log.get_logger(obj=obj)
        if len(args) > 1:
            logger.info(args[0], args[1:])
        else:
            logger.info(args[0])

    @staticmethod
    def error(obj, *args):
        """Prints error messages

        :param obj: the object/string to log
        :param args: the arguments to set within the string - works like c-style printf %s/%d/...
        :return: None
        """
        logger = Log.get_logger(obj=obj)
        if len(args) > 1:
            logger.error(args[0], args[1:])
        else:
            logger.error(args[0])
