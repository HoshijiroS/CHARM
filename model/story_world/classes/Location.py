class Location:
    name = ""
    appProp = []
    perProp = []
    amtProp = []
    attr = []

    def __init__(self, name):
        self.name = name
        self.appProp = []
        self.perProp = []
        self.amtProp = []
        self.attr = []

    def hasAppProperty(self, prop, scene):
        propPair = [prop, scene]
        self.appProp.append(propPair)

    def hasPerProperty(self, prop, scene):
        propPair = [prop, scene]
        self.perProp.append(propPair)

    def hasAmtProperty(self, prop, scene):
        propPair = [prop, scene]
        self.amtProp.append(propPair)

    def hasAttribute(self, attribute, action, scene):
        attrPair = [action, attribute, scene]
        self.attr.append(attrPair)

    def queryProperty(self, prop_name, type_name, scene_name):
        # entity[0] = property
        # entity[1] = scene

        if type_name is not None:
            if type_name == "personality":
                if scene_name is None:
                    for entity in self.perProp:
                        for items in entity[0]:
                            if items == prop_name:
                                return entity[0], entity[1]

                elif prop_name is None:
                    for entity in self.perProp:
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

            elif type_name == "appearance":
                if scene_name is None:
                    for entity in self.appProp:
                        for items in entity[0]:
                            if items == prop_name:
                                return entity[0], entity[1]

                elif prop_name is None:
                    for entity in self.appProp:
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

            elif type_name == "amount":
                if scene_name is None:
                    for entity in self.amtProp:
                        for items in entity[0]:
                            if items == prop_name:
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
