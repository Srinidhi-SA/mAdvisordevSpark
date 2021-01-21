from __future__ import print_function

from builtins import object
class Node(object):
    name = "name"
    slug = "slug"
    listOfNodes = []
    listOfCards = []

    def __init__(self, name, slug, listOfNodes=[], listOfCards=[]):
        self.name = name
        self.slug = slug
        self.listOfNodes = listOfNodes
        self.listOfCards = listOfCards


class Card(object):
    name = ""
    slug = ""
    cardType = ""
    cardData = {}

    def __init__(self, name, slug, cardType):
        self.name = name
        self.slug = slug
        self.cardType = cardType
        self.cardData = {
        "noOfDimensions": 8,
        "noOfMeasures":  10,
        "summaryHtml": "summary with HTML <b>tags</b>",
        "quotesHtml": "Quote that comes on the right side"
        }


if __name__ == "__main__":
    c1 = Card("summary", "summary", "summary")
    c2 = Card("overview", "overview", "executivesummary")
    
    ct1 = Card("trend1", "trend1", "normal")
    ct2 = Card("trend2", "trend2", "normal")
    ct3 = Card("trend3", "trend3", "normal")


    cp = Card("PerformanceOverview", "performanceOverview", "normal")
    cp1 = Card("performance1", "performance1", "normal")
    cp2 = Card("performance2", "performance2", "normal")
    cp3 = Card("performance3", "performance3", "Nornormalmal")


    n1 = Node("overview","overview",[],[c2,])
    n2 = Node("trend","trend",[],[ct1,ct2,ct3])

    np1 = Node("AverageNumber1","AverageNumber1",[],[cp1,cp2,cp3])
    np2 = Node("AverageNumber2","AverageNumber2",[],[cp1,cp2,cp3])
    np3 = Node("AverageNumber3","AverageNumber3",[],[cp1,cp2,cp3])


    n3 = Node("performance","performance",[np1,np2,np3],[cp])
    n4 = Node("influencer","influencer",[],[c1,c2,])
    # n5 = Node("predictions","predictions",[],[c1,c2])
    


    root = Node("SignalsRoot","Signals",[n1,n2,n3,n4],[c1])
    # root = Node("SignalsRoot","Signals",[n1,],[])
    
    import json
    print(json.dumps(root, default=lambda o: o.__dict__))

    pass
