''' ====================================================================
    Utility script for myclimbs.
        Functions:
            readClimbs() - Function to read CSV climbing log
            plotDistanceBySession() - Generates a graph showing distance by
                session
            plotVSumsBySession() - Generates a graph showing VSums by session
    ===================================================================='''
import re
import csv
import session
import climb
import exceptions
import math
import matplotlib.pyplot as plt
import numpy as np

''' A function used to read and parse a climbing log csv (template)
    for myclimbs.
        In:
            dateRange (year)
            climbTrackerFilePath - The path to the csv file
        Out:
            A list of sessions.
'''


def readClimbs(dateRange, climbTrackerFilePath):
    sessions = []
    thisClimb = ()
    thisSession = ()
    thisSessionDate = ""
    lastSessionDate = ""

    with open(climbTrackerFilePath) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:

            if dateRange in row["Date"]:
                thisSessionDate = row["Date"]

                # If session ended last iteration, add it and create a new one
                if thisSessionDate != lastSessionDate:
                    if lastSessionDate != "":
                        sessions.append(thisSession)

                    # Append session for first case and when date changes
                    thisSession = session.Session(thisSessionDate)

                # Construct climb object based on type
                if row["Type"] == "B":
                    thisClimb = climb.Boulder(row["Grade"], row["# RP Tries"],
                                              row["Type"], row["Length"],
                                              row["Laps"])
                    thisSession.addBoulder(thisClimb)
                # TODO need to finish winter implementation, ran out of LOCs
                if row["Type"] == "W":
                    pass
                    # Construct Winter Climb
                else:
                    thisClimb = climb.Climb(row["Grade"], row["# RP Tries"],
                                            row["Type"], row["Length"],
                                            row["Laps"])
                    thisSession.addClimb(thisClimb)

                lastSessionDate = row["Date"]

        # Add the last session
        # try:
        sessions.append(thisSession)
        # except NoClimbsInPeriodError:
        # print("There aren't any climbs/sessions logged in ", dateRange)

    return sessions


''' Function to plot distance by session date.
        In:
            sessions - list of session type'''


def plotDistanceBySession(sessions):
    dates = []
    distances = []
    maxSessionDistance = 0

    fig = plt.figure(dpi=150)  # 150 DPI equal "good enough" size
    # The next line is very important. Without it, axis labels don't show.
    ax = fig.add_subplot(111)

    for session in sessions:
        dates.append(session.getSessionDate())
        distances.append(session.getSessionDistance())
        if session.getSessionDistance() > maxSessionDistance:
            maxSessionDistance = session.getSessionDistance()

    # Have to get data ordered (by dates) from first of year to EOY
    dates.reverse()
    distances.reverse()

    ax.set_title('Total Vertical Distance Climbed by Session Date')
    ax.set_ylabel('Session Distances (Feet)')
    ax.set_yticks(np.arange(0, maxSessionDistance, 40))
    ax.set_xlabel('Session Dates')
    ax.set_xticklabels(dates, rotation=90)
    ax.bar(dates, distances)
    fig.tight_layout()

    plt.show()


''' Function to plot VSums by session date.
        In:
            sessions - list of session type'''


def plotVSumsBySession(sessions):
    dates = []
    vsums = []
    maxSessionVSum = 0

    fig = plt.figure(dpi=150)  # 150 DPI equal "good enough" size
    # The next line is very important. Without it, axis labels don't show.
    ax = fig.add_subplot(111)

    for session in sessions:
        if "B" in session.getSessionType():
            if session.getSessionVSum() > 0:
                dates.append(session.getSessionDate())
                vsums.append(session.getSessionVSum())
                if session.getSessionVSum() > maxSessionVSum:
                    maxSessionVSum += session.getSessionVSum()

    # Have to get data ordered (by dates) from first of year to EOY
    dates.reverse()
    vsums.reverse()

    ax.set_title('VSums by Session Date')
    ax.set_ylabel('VSum')
    ax.set_yticks(np.arange(0, maxSessionVSum, 5))
    ax.set_xlabel('Session Date')
    ax.set_xticklabels(dates, rotation=90)
    ax.bar(dates, vsums)
    fig.tight_layout()

    plt.show()


''' Function to plot grade pyramid for bouldering and summer roped climbs.
        In:
            sessions - list of session type
'''


def plotClimbPyramids(sessions):

    boulderGradeCount = {}
    summerRopedGradeCount = {}

    for session in sessions:
        sessionGradeCount = session.getSessionGradeCount()

        # print(session.getSessionType())
        # if session.

        for grade, gradecount in sessionGradeCount.items():

            # If this is a bouldering session
            # if session.getSessionVSum() > 0:
            if "V" in grade and "x" in grade:
                # Strip x out of grade and build dict
                grade = grade.replace("x", "")
                if grade in boulderGradeCount.keys():
                    boulderGradeCount[grade] += gradecount
                else:
                    boulderGradeCount[grade] = gradecount
            # TODO need to finish winter implementation, ran out of LOCs
            # If this is a summer roped session
            else:
                if "5." in grade and "x" in grade:
                    # Strip x out of grade and build dict
                    grade = grade.replace("x", "")
                    if grade in summerRopedGradeCount.keys():
                        summerRopedGradeCount[grade] += gradecount
                    else:
                        summerRopedGradeCount[grade] = gradecount

    # Call the plotting function
    plotPyramid(boulderGradeCount, "Bouldering Pyramid")
    plotPyramid(summerRopedGradeCount, "Summer Roped Pyramid")


''' A generic pyramid plot function used for all session types
    Input:
        gradeCount dict
        title for graph
    Output:
        pyramid bar chart
'''


def plotPyramid(gradeCount, title):
    maxCount = max(gradeCount.values())
    gradeCountSorted = {}
    fig = plt.figure(dpi=150)  # 150 DPI equal "good enough" size

    # The next line is very important. Without it, axis labels don't show.
    ax = fig.add_subplot(111)

    # gradeCountSorted = OrderedDict(sorted(gradeCount.items()))

    # This is a super hacky way of performing a natural sort without natsort
    gradeCountSortedKeyList = natural_sort(gradeCount.keys())

    for key in gradeCountSortedKeyList:
        gradeCountSorted[key] = gradeCount[key]

    # Dynamically generate y tick spacing base on maxCount
    ytickStep = int(math.ceil(maxCount / 10))

    # Generate plot
    ax.set_title(title)
    ax.set_ylabel('Count')
    ax.set_yticks(np.arange(0, maxCount, ytickStep))
    ax.set_xlabel('Grade')
    ax.set_xticklabels(list(gradeCountSorted.keys()))
    ax.bar(list(gradeCountSorted.keys()), list(gradeCountSorted.values()),
           align='center')
    fig.tight_layout()
    plt.show()


''' A function to sort string in natural order.
        This is used to handle tricky problem of sorting Yosemite climbing
            grades.
        From:
            https://stackoverflow.com/questions/4836710/is-there-a-built-in- +
            function-for-string-natural-sort
        Since we could not use third party utils like natsort.
'''


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)
