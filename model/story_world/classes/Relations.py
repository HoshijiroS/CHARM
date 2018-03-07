class Relations:
    sceneName = ""
    elabList = []
    causeList = []
    contList = []
    consList = []
    summary = []

    def __init__(self, sceneName):
        self.sceneName = sceneName
        self.causeList = []
        self.contList = []
        self.consList = []
        self.summary = []

    def causedBy(self, a, bList):
        self.causeList.append([a, bList])

    def contradiction(self, a, b):
        self.contList.append([a, b])

    def consequence(self, a, b):
        self.consList.append([a, b])

    def sequence(self, a, b):
        self.summary.append([a, b])
