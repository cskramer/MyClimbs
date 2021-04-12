''' ====================================================================
    Climb: A generic climb class, used primarily for Summer
            Ropes Climbs (Sport, Top Rope, Trad).
        Methods:
            __init__() - constructor
            getTotalLength() - Method to get the total length of the climb
    ===================================================================='''


class Climb():

    # Constructor method for the Climb class.
    def __init__(self, grade, tries, climbType, length, laps):
        grade.upper()
        grade = grade.replace("X", "")
        self.grade = grade
        self.tries = tries
        self.climbType = climbType
        self.length = length
        self.laps = laps

    # Get the total lenth of a climb (length * laps)
    def getTotalLength(self):
        ''' Using the climbingLog template, a "%" in the "tries"
                    column indicates that the climb was not successful '''
        if "%" not in self.tries:
            return int(self.length) * int(self.laps)
        else:
            return 0


''' ====================================================================
    Boulder: An extension of the Climb class, used for bouldering
            routes (no rope, different grades and reports).
        Methods:
            __init__() - constructor
            getVSum() - Method to get the vsum coefficient
    ==================================================================== '''


class Boulder(Climb):

    ''' Constructor method for the Boulder class. Also called
                instructor for base class ("Climb") '''
    def __init__(self, grade, tries, climbType, length, laps):
        Climb.__init__(self, grade, tries, climbType, length, laps)
        self.vsum = self.getVSum()

    def getVSum(self):
        tempgrade = self.grade.replace("x", "")

        # If the climb was completed
        if "%" not in self.tries:
            if tempgrade == "V1" \
                    or tempgrade == "5":
                return 1
            elif tempgrade == "V2" \
                    or tempgrade == "5+":
                return 2
            elif tempgrade == "V3" \
                    or tempgrade == "6A" \
                    or tempgrade == "6A+":
                return 3
            elif tempgrade == "V4" \
                    or tempgrade == "6B" \
                    or tempgrade == "6B+":
                return 4
            elif tempgrade == "V5" \
                    or tempgrade == "6C" \
                    or tempgrade == "6C+":
                return 5
            elif tempgrade == "V6" \
                    or tempgrade == "7A":
                return 6
            elif tempgrade == "V7" \
                    or tempgrade == "7A+":
                return 7
            elif tempgrade == "V8" \
                    or tempgrade == "7B" \
                    or tempgrade == "7B+":
                return 8
            elif tempgrade == "V9" \
                    or tempgrade == "7C":
                return 9
            elif tempgrade == "V10" \
                    or tempgrade == "7C+":
                return 10
            elif tempgrade == "V11" \
                    or tempgrade == "8A":
                return 11
            elif tempgrade == "V12" \
                    or tempgrade == "8A+":
                return 12
            elif tempgrade == "V13" \
                    or tempgrade == "8B":
                return 13
            elif tempgrade == "V14" \
                    or tempgrade == "8B+":
                return 14
            elif tempgrade == "V15" \
                    or tempgrade == "8C":
                return 15
            elif tempgrade == "V16" \
                    or tempgrade == "8C+":
                return 16
            else:
                return 0
        else:
            return 0
