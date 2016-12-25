#!/usr/bin/env python3

"""This module will give you an idea of OOP and python.

 Just look at the aesthetics of the class and functions and you may get the idea ; )
"""
__version__ = "1.0"

# Author: nico & wolf


class Contact(object):
    """This class holds contact information and is an example

    This class holds information about people and their contact information: first- and last name,
     the cell phone number and the email address.
    """
    def __init__(self, first_name, last_name, cellphone_number="", email_adr=""):
        """Initializes and declares class attributes from the given parameters

        :param first_name: The first name of the contact
        :param last_name: The last name of the contact
        :param cellphone_number: The cellphone number of the contact
        :param email_adr: The e-mail address of the contact
        """

        # those are "private" member (the underscore signals "private")
        self._first_name = first_name
        self._last_name = last_name
        self._cell_phone = cellphone_number
        self._email_adr = email_adr

    @property
    def get_name(self):
        """This is the name property and returns the name

        :return: first_name + ' ' + last_name
        """
        return self._first_name + ' ' + self._last_name

    def set_cellphone_number(self, cellphone_number):
        self._cell_phone = cellphone_number


