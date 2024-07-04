#!/usr/bin/env python3
""" Regex-ing module """
import logging
import re


def filter_datum(fields, redaction, message, separator):
    """ returns the log message """
    for field in fields:
        pattern = r"{}=.*?{}".format(field, separator)
        rep = r"{}={}{}".format(field, redaction, separator)
        message = re.sub(pattern, rep, message)
    return message
