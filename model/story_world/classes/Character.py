class Character:
    name = ""
    charType = []
    gender = ""
    state = []
    appProp = []
    perProp = []
    amtProp = []
    attr = []
    loc = []
    act = []
    des = []
    rel = []

    def __init__(self, name, gender, charType):
        self.name = name
        self.charType = charType
        self.gender = gender
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

        act, attr, ev = self.queryAttribute(None, attribute.name, None)

        return attr

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
        for entity in self.charType:
            if entity == type_name:
                return entity
        return None

    def queryState(self, state_name, scene_name):
        # entity[0] = state
        # entity[1] = scene

        if scene_name is None:
            for entity in self.state:
                for action in entity[0]:
                    if action == state_name:
                        return entity[0], entity[1]

        elif state_name is None:
            for entity in self.state:
                if entity[1] == scene_name:
                    return entity[0], entity[1]

        return None, None

    def queryProperty(self, prop_name, type_name, scene_name):
        # entity[0] = property
        # entity[1] = scene

        if type_name is not None:
            if type_name == "personality":
                if scene_name is None:
                    for entity in self.perProp:
                        if entity[0] == prop_name:
                            return entity[0], entity[1]

                elif prop_name is None:
                    for entity in self.perProp:
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

            elif type_name == "appearance":
                if scene_name is None:
                    for entity in self.appProp:
                        if entity[0] == prop_name:
                            return entity[0], entity[1]

                elif prop_name is None:
                    for entity in self.appProp:
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

            elif type_name == "amount":
                if scene_name is None:
                    for entity in self.amtProp:
                        if entity[0] == prop_name:
                            return entity[0], entity[1]

                elif prop_name is None:
                    for entity in self.amtProp:
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

        return None, None

    def queryAttribute(self, act_name, attr_name, ev_name):
        # entity[0] = actions
        # entity[1] = attribute
        # entity[2] = scene

        if act_name is None and ev_name is None:
            for entity in self.attr:
                if entity[1].name.lower() == attr_name.lower():
                    return entity[0], entity[1], entity[2]

        elif act_name is None and attr_name is None:
            for entity in self.attr:
                if entity[2] == ev_name:
                    return entity[0], entity[1], entity[2]

        return None, None, None

    def queryLocation(self, act_name, loc_name):
        # entity[0] = actions
        # entity[1] = location
        # entity[2] = scene

        if loc_name is None:
            # print("here")
            for entity in self.loc:
                for action in entity[0]:
                    if action == act_name:
                        return entity[1], entity[2]

        else:
            for entity in self.loc:
                if entity[1].name.lower() == loc_name.lower():
                    for action in entity[0]:
                        if action == act_name:
                            return entity[1], entity[2]

        return None, None

    def queryDesire(self, act_name):
        # entity[0] = actions
        # entity[1] = object
        # entity[2] = scene

        for entity in self.des:
            for action in entity[0]:
                if action == act_name:
                    return entity[1], entity[2]

        return None, None

    def queryAction(self, act_name, scene_name):
        # entity[0] = actions
        # entity[1] = object
        # entity[2] = scene

        if scene_name is None:
            for entity in self.act:
                for action in entity[0]:
                    if action == act_name:
                        return entity[0], entity[1], entity[2]

        elif act_name is None:
            for entity in self.act:
                if entity[2] == scene_name:
                    return entity[0], entity[1], entity[2]

        return None, None, None

    def queryRelationship(self, char_name, rel_name):
        # entity[0] = person
        # entity[1] = relationship

        dummyNames = []
        dummyRels = []
        if char_name is None:
            for entity in self.rel:
                if type(entity[1]) is not str:
                    for rels in entity[1]:
                        if rels.lower() == rel_name:
                            dummyNames.append(entity[0])
                            dummyRels.append(entity[1])

                else:
                    if entity[1].lower() == rel_name:
                        dummyNames.append(entity[0])
                        dummyRels.append(entity[1])

            return dummyNames, dummyRels

        elif rel_name is None:
            for entity in self.rel:
                if entity[0].name.lower() == char_name.lower():
                    return entity[0], entity[1]

        return None, None
