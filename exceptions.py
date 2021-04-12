'''====================================================================
    Script to hold exception classes for myclimbs
    ==================================================================== '''


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidYearError(Exception):
    """Raised when user aattempts to analyze climbs from an invalid year.
       Should work for years 1900/current year."""
    pass


class InvalidCSVPathError(Exception):
    """Raised when user provides an invalid path to csv file. """
    pass


class NoClimbsInPeriodError(Exception):
    """Raised when period does not contain any climbs/sessions"""
    pass
