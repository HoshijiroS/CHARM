class Scene:
    name = ""
    char = []
    loc = []
    time = ""

    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.char = []
        self.loc = []

    def hasLocation(self, loc):
        self.loc.append(loc)

    def hasCharacter(self, char):
        self.char.append(char)

    def hasEvents(self, event):
        self.events.append(event)

    def hasInformation(self, info):
        self.infos.append(info)