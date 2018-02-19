class Character:
    name = ""
    type = []
    state = []
    appProp = []
    perProp = []
    amtProp = []
    attr = []
    loc = []
    act = []
    des = []
    rel = []

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.state = []
        self.appProp = []
        self.perProp = []
        self.amtProp = []
        self.attr = []
        self.loc = []
        self.act = []
        self.des = []
        self.rel = []

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

    def hasLocation(self, location, action, scene):
        locPair = [action, location, scene]
        self.loc.append(locPair)

        return location

    def hasAttribute(self, attribute, action, scene):
        attrPair = [action, attribute, scene]
        self.attr.append(attrPair)

        value = self.queryAttribute(None, attribute.name)

        return value

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

        #print("states: ", self.state)
        if state_name is not None:
            for entity in self.state:
                print("entity: ", entity)
                print("entity[0]: ", entity[0], " vs state_name: ", state_name)
                for action in entity[0]:
                    if action == state_name:
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

    def queryAttribute(self, act_name, attr_name):
        # entity[0] = actions
        # entity[1] = attribute
        # entity[2] = scene

        if act_name is None:
            for entity in self.attr:
                #print("entity[1]: ", entity[1], " and ", attr_name)
                if entity[1].name.lower() == attr_name.lower():
                    return entity[1]
        else:
            for entity in self.attr:
                if entity[1].name.lower() == attr_name.lower():
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
                if entity[1].name.lower() == loc_name.lower():
                    for action in entity[0]:
                        if action == act_name:
                            return entity[1], entity[2]

        elif loc_name is None:
            #print("here")
            for entity in self.loc:
                for action in entity[0]:
                    #print("action: ", action, " and ", act_name)
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

        return None

    def queryAction(self, act_name):
        # entity[0] = actions
        # entity[1] = object
        # entity[2] = scene

        for entity in self.act:
            #print("entity: ", entity)
            for action in entity[0]:
                #print("action: ", action, " vs ", "act_name: ", act_name)
                if action == act_name:
                    return entity[1], entity[2]

        return None

    def queryRelationship(self, char_name, rel_name):
        # entity[0] = person
        # entity[1] = relationship

        if rel_name is not None:
            for entity in self.rel:
                if entity[1].lower() == rel_name:
                    return entity[0]

        if char_name is not None:
            for entity in self.rel:
                #print(entity[0], " vs ", char_name)
                if entity[0].lower() == char_name.lower():
                    return entity[1]

        return None