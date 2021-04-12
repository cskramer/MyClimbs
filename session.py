''' ====================================================================
    Session: A class to represent a instance of a climbing session.
        A climbing session consists of:
            A unique climbing date
            1 or more climb instances
        Methods:
            __init__ - Constructor for the class
            updateSessionType() - Updates session type information for
                    climbs if necessary. Each session can have multiple
                    climb types.
            updateSessionGradeCount() - Updated the count of successful
                    climbs for each grade
            addClimb() - Add a climb type to session
            getSessionType() - Returns type of session. Can have more
                    than one type per session (example: "BS").
                    B = Bouldering
                    S = Summer
                    W = Winter
            getSessionVSum() - Returns the VSum for the session (if
                    Bouldering occured in session)
            getSessionGradeCount() - Provides a count/distrobution of
                    all grades
            getSessionDistance(unit) - Return the sum of the lengths
                    of all successful climbs in a session
            getSessionDate - Returns the date of the session
    ===================================================================='''


class Session():

    climbs = []
    sessionType = ""
    totalDistance = 0
    vSum = 0
    sessionGradeCount = {}

    # Constructor method for the Session class.
    def __init__(self, date):
        self.date = date
        self.sessionGradeCount = {}
        self.vSum = 0
        self.totalDistance = 0
        self.climbs = []
        self.sessionType = ""

    # Update session type information (sessionType) by appending it to string
        # Climb types are: B, TR, Trad, SP, MI, WI
    def updateSessionType(self, climb):

        if climb.climbType not in self.sessionType:
            self.sessionType += climb.climbType

        # Winter climbs - look at winter grades to determine winter sessions
        if "WI" in climb.grade and "WI" not in self.sessionType:
            self.sessionType += "WI"
        if "MI" in climb.grade and "MI" not in self.sessionType:
            self.sessionType += "MI"

    # Update session grade count dictionary (sessionGradeCount)
    def updateSessionGradeCount(self, climb):
        if climb.grade in self.sessionGradeCount:
            self.sessionGradeCount[climb.grade] += 1
        else:
            self.sessionGradeCount[climb.grade] = 1

    # Add a climb to this session
    def addClimb(self, climb):
        self.climbs.append(climb)
        self.totalDistance += climb.getTotalLength()
        self.updateSessionType(climb)
        self.updateSessionGradeCount(climb)

    # Add a climb to this session
    def addBoulder(self, climb):
        self.updateSessionType(climb)
        self.vSum += climb.getVSum()

    ''' Returns the session type (sessionType).
        A session can consist of more than one type of climb '''
    def getSessionType(self):
        return self.sessionType

    ''' Returns a dictionary (sessionGradeCount) containing
        counts of successful climbs for each grade in a session '''
    def getSessionGradeCount(self):
        return self.sessionGradeCount

    ''' Returns the VSum (vSum) for the session '''
    def getSessionVSum(self):
        return self.vSum

    ''' Return the total distance (totalDistance) for the session '''
    def getSessionDistance(self):
        return self.totalDistance

    ''' Return the date of the session '''
    def getSessionDate(self):
        return self.date
