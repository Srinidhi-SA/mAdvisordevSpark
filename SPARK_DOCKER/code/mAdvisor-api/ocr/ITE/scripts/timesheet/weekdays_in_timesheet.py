# -*- coding: utf-8 -*-
import itertools
import re
from itertools import compress


class weekdays_timesheet():
    def __init__(self):
        pass

    def check_days(self, analysis):

        weekday_match = re.compile('mon|tue|wed|thu|fri|sat|sun|tot|sum')
        weekday_match2 = re.compile('^mo$|^tu$|^we$|^th$|^fr$|^sa$|^su$')
        weekdays = []
        wc = {}
        for i, line in enumerate(analysis["lines"]):
            wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

        for line in wc:

            present_line = wc[line]
            for bb, word in present_line:

                if weekday_match.search(word.lower()) or weekday_match2.search(word.lower()):
                    weekdays.append((bb, word))
        if weekdays:
            return True, weekdays
        else:
            return False, weekdays

    def check_orientation(self, polygons):

        X_centroids = []
        Y_centroids = []

        for i in range(len(polygons)):
            cords = polygons[i][0]
            p1, p2, p3, p4 = cords[:2], cords[2:4], cords[4:6], cords[6:8]
            centroid_x = (p1[0] + p3[0]) * 0.5
            centroid_y = (p1[1] + p3[1]) * 0.5
            X_centroids.append(centroid_x)
            Y_centroids.append(centroid_y)

        if (len(set(X_centroids)) < len(X_centroids)):
            return 'vertical'

        elif (len(set(Y_centroids)) < len(Y_centroids)):

            return 'horizontal'

        else:

            def sumPairs(lst):
                diffs = [abs(e[1] - e[0]) for e in itertools.permutations(lst, 2)]
                return int(sum(diffs))

            #            print('It came here')
            if sumPairs(X_centroids) > sumPairs(Y_centroids):

                return 'horizontal'

            else:

                return 'vertical'
