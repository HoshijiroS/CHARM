class Item:
    name = ""
    appProp = []
    perProp = []
    amtProp = []
    state = []
    pur = []

    def __init__(self, name):
        self.name = name
        self.appProp = []
        self.perProp = []
        self.amtProp = []
        self.state = []
        self.pur = []

    def hasPurpose(self, action, obj, scene):
        purPair = [action, obj, scene]
        self.pur.append(purPair)

    def hasState(self, state, scene):
        statePair = [state, scene]
        self.state.append(statePair)

    def hasAppProperty(self, prop, scene):
        propPair = [prop, scene]
        self.appProp.append(propPair)

    def hasPerProperty(self, prop, scene):
        propPair = [prop, scene]
        self.perProp.append(propPair)

    def hasAmtProperty(self, prop, scene):
        propPair = [prop, scene]
        self.amtProp.append(propPair)

    def queryState(self, state_name, scene_name):
        # entity[0] = state
        # entity[1] = scene

        if state_name is not None:
            for entity in self.state:
                if entity[0] == state_name:
                    return entity[1]

        if scene_name is not None:
            for entity in self.state:
                if entity[1] == scene_name:
                    return entity[0]

        return None

    def queryProperty(self, prop_name, type_name, scene_name):
        # entity[0] = property
        # entity[1] = type
        # entity[2] = scene

        if prop_name is not None:
            for entity in self.prop:
                if entity[0] == prop_name:
                    return entity[1], entity[2]

        if scene_name is not None:
            for entity in self.prop:
                if entity[2] == scene_name:
                    return entity[0]

        if type_name is not None:
            for entity in self.prop:
                if entity[1] == type_name:
                    return entity[0]

        return None
