class Character:
    name = ""
    type = []
    state = []
    prop = []
    attr = {}
    loc = []
    act = []
    des = []
    rel = []

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.prop = []
        self.attr = []
        self.loc = []
        self.act = []
        self.des = []
        self.rel = []

    def hasState(self, state, scene):
        statePair = [state, scene]
        self.state.append(statePair)

    def hasProperty(self, prop, scene):
        propPair = [prop, scene]
        self.prop.append(propPair)

    def hasLocation(self, location, action, scene):
        locPair = [action, location, scene]
        self.loc.append(locPair)

        return location

    def hasAttribute(self, attribute, action, scene):
        attrPair = [action, attribute, scene]
        self.attr.append(attrPair)

        return attribute

    def hasAction(self, action, obj, scene):
        actPair = [action, obj, scene]
        self.act.append(actPair)

    def hasDesire(self, action, obj, scene):
        desPair = [action, obj, scene]
        self.des.append(desPair)

    def hasRelationship(self, char, relationship):
        relPair = [char, relationship]
        self.rel.append(relPair)

    def queryType(self, type_name):
        for entity in self.type:
            if entity == type_name:
                return entity
        return None

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

    def queryAttribute(self, act_name, attr_name):
        # entity[0] = actions
        # entity[1] = attribute
        # entity[2] = scene

        for entity in self.attr:
            if entity[1] == attr_name:
                for action in entity[0]:
                    if action == act_name:
                        return entity[1], entity[2]
        return None

    def queryLocation(self, act_name, loc_name):
        # entity[0] = actions
        # entity[1] = location
        # entity[2] = scene
        if loc_name is not None:
            for entity in self.loc:
                # print("entity: ")
                # print(entity[1].name)
                # print("loc name: ")
                # print(loc_name)
                if entity[1].name == loc_name:
                    for action in entity[0]:
                        # print("action: ")
                        # print(action)
                        if action == act_name:
                            return entity[1], entity[2]
        else:
            for entity in self.loc:
                for action in entity[0]:
                    if action == act_name:
                        return entity[1], entity[2]
        return None

    def queryDesire(self, act_name):
        # entity[0] = actions
        # entity[1] = object
        # entity[2] = scene

        for entity in self.des:
            for action in entity[0]:
                if action == act_name:
                    return entity[1], entity[2]
                else:
                    return None

        return None

    def queryRelationship(self, char_name, rel_name):
        # entity[0] = person
        # entity[1] = relationship

        if rel_name is not None:
            for entity in self.rel:
                if entity[1] == rel_name:
                    return entity[0]

        if char_name is not None:
            for entity in self.rel:
                if entity[0] == char_name:
                    return entity[1]

        return None
