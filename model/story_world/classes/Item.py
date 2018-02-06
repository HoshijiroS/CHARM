class Item:
    name = ""
    prop = []
    state = []
    pur = []

    def __init__(self, name):
        self.name = name
        self.prop = []
        self.state = []
        self.pur = []

    def hasPurpose(self, action, obj, scene):
        purPair = [action, obj, scene]
        self.pur.append(purPair)

    def hasState(self, state, scene):
        statePair = [state, scene]
        self.state.append(statePair)

    def hasProperty(self, prop, scene):
        propPair = [prop, scene]
        self.prop.append(propPair)

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

    def queryProperty(self, prop_name, scene_name):
        # entity[0] = property
        # entity[1] = scene

        if prop_name is not None:
            for entity in self.prop:
                if entity[0] == prop_name:
                    return entity[1]

        if scene_name is not None:
            for entity in self.prop:
                if entity[1] == scene_name:
                    return entity[0]

        return None
