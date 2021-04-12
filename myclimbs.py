from utility import *
from datetime import datetime
from exceptions import *
import os.path
import session


''' The mains driver method for MyClimbs.
        1. Requests and validate csv file path and year to be analyzed
        2. Calls utility.readClimbs to generate Session list
        3. Calls graphing functions in utility
        4. Displays text summary of metrics for period

    TODOs:
        1. Handle winter climbs
        2. VSum might be off for a couple of sessions.
            Example: 2021.02.20
            Might be a problem with how data was entered in spreadsheet
        3. Shrink font on graphs when range is more than year

    Test Files:
        'IndoorClimbingLog.csv'
        'OutdoorClimbingLog.csv'
'''


def main():

    # Validate CSV file path
    while True:
        # Prompt for the path of a file
        climbTrackerFilePath = input("Please enter a path to your csv file: ")

        if not os.path.exists(climbTrackerFilePath):
            print("The CSV logger path entered (", climbTrackerFilePath,
                  ") is invalid, or no readable csv file found.")
            continue
        break

    # Validate year
    while True:
        # Prompt the user for the year(s) they want to analyze
        dateRange = input('''Please enter the year you would like to analyze.
        Just press enter to analyze all years (Example: 2021): ''')

        if dateRange != "":
            if int(dateRange) < 1900 or int(dateRange) > datetime.now().year:
                print("Please enter a year between 1900 and ",
                      datetime.now().year)
                continue
        break

    totalClimbLength = 0
    numBoulderingSessions = 0
    numSummerRopeSessions = 0
    numWinterRopeSessions = 0

    # Generate sessions/class heirarchy using the readClimbs utility
    sessions = readClimbs(dateRange, climbTrackerFilePath)

    # If we have empty csv, or only a header row and no data
    if len(sessions) <= 1:
        print("Did not find any climbing sessions in ", dateRange)
        raise NoClimbsInPeriodError

    # Generate plots
    plotDistanceBySession(sessions)
    plotVSumsBySession(sessions)
    plotClimbPyramids(sessions)

    for session in sessions:

        # Count Bouldering sessions
        if "B" in session.getSessionType():
            numBoulderingSessions += 1

        # Count summer roped sessions
        summerRoped = ["TR", "SP", "Trad", "L"]
        if any(x in session.getSessionType() for x in summerRoped):
            numSummerRopeSessions += 1

        # Count summer roped sessions
        # TODO need to finish winter implementation, ran out of LOCs
        winterRoped = ["WI", "MI"]
        if any(x in session.getSessionType() for x in winterRoped):
            numWinterRopeSessions += 1

        totalClimbLength += session.getSessionDistance()

    # Print out results
    print("\nAnalyzing climbs and generating reports ........")
    print("\n--- Number of climbing sessions:", len(sessions))
    print("   --- Number of bouldering sessions:", numBoulderingSessions)
    print("   --- Number of TR/Sport/Trad sessions:", numSummerRopeSessions)
    print("   --- Number of Winter Ropes sessions:", numWinterRopeSessions)
    print("\n--- Total vertical distance climbed:", totalClimbLength)


if __name__ == '__main__':
    main()
