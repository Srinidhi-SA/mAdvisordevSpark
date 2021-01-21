# -*- coding: utf-8 -*-
import re


class dates_timesheet():
    def __init__(self):
        pass

    def date_extractor(self, analysis):

        #        date_match = re.compile(r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+|[\d]{1,2}/[\d]{1,2}')
        #        date_match2 = re.compile(r'^[1-9]$|[1-2][0-9]$|3[01]$')
        #        date_match=date_match=re.compile(r'(\d{2,4}[/-]|)([0-3]|)\d[/-]([0-3]|)\d')
        #        date_match=re.compile(r'((\d{2,4}[/-]|)([0-3]|)\d[/-]([0-3]|)\d)|(^\b\d{1}\b$)|(\d\d[-/][jfmasond][aepuco][nbrylgptvc][-/]20[1-2]\d)')
        date_match = re.compile(
            r'((\d{2,4}[/-]|)([0-3]|)\d[/-]([0-3]|)\d)|(\d\d[-/][jfmasond][aepuco][nbrylgptvc][-/]20[1-2]\d)|([jfmasond][aepuco][nbrylgptvc][-/][\d|]\d)')

        dates = []
        wc = {}
        for i, line in enumerate(analysis["lines"]):
            wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

        for line in wc:

            present_line = wc[line]
            for bb, word in present_line:

                if date_match.search(word.lower()):
                    dates.append((bb, word))
        if dates:
            return True, dates
        else:
            return False, dates

    def special_date_extractor(self, analysis):

        date_match = re.compile(r'jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec')

        special_dates = []
        wc = {}
        for i, line in enumerate(analysis["lines"]):
            wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

        for line in wc:

            present_line = wc[line]
            for bb, word in present_line:

                if date_match.search(word.lower()):
                    special_dates.append((bb, word))

        if special_dates:
            return True, special_dates
        else:
            return False, special_dates

    def centroid(self, bb):

        return (int((bb[0] + bb[4]) * 0.5), int((bb[1] + bb[5]) * 0.5))

    def check_orientation(self, l):  # DATES

        if len(l) >= 2:
            centroids = [self.centroid(bb) for bb, txt in l]

            xs = [cen[0] for cen in centroids]
            ys = [cen[1] for cen in centroids]

            #        print(xs)
            #        print(ys)
            modex = max(set(xs), key=xs.count)
            modey = max(set(ys), key=ys.count)

            #        print('MODEX:' ,modex,'MODEY:',modey)
            #        print('X VALS:',[x-modex for x in xs])
            #        print('Y VALS:',[y-modey for y in ys])
            x_oriented = sum([True if abs(x - modex) < 10 else False for x in xs]) > 3
            y_oriented = sum([True if abs(y - modey) < 10 else False for y in ys]) > 3

            if x_oriented:
                return "vertical"
            elif y_oriented:
                return "horizontal"
            else:
                return "No Orientation"
        else:
            return "Too few Dates"
