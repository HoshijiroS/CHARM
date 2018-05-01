class Item:
    name = ""
    appProp = []
    perProp = []
    amtProp = []
    state = []
    act = []

    def __init__(self, name):
        self.name = name
        self.appProp = []
        self.perProp = []
        self.amtProp = []
        self.state = []
        self.act = []

    def hasAction(self, action, obj, scene):
        actPair = [action, obj, scene]
        self.act.append(actPair)

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

        if scene_name is None:
            for entity in self.state:
                for action in entity[0][1]:
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
                print("personality")
                print("scene_name: ", scene_name)
                if scene_name is None:
                    for entity in self.perProp:
                        for items in entity[0]:
                            if items == prop_name:
                                return entity[0], entity[1]

                elif scene_name:
                    print("scene in personality")
                    for entity in self.perProp:
                        print("entity[1]: ", entity[1])
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

            elif type_name == "appearance":
                print("appearance")
                if scene_name is None:
                    for entity in self.appProp:
                        for items in entity[0]:
                            if items == prop_name:
                                return entity[0], entity[1]

                elif scene_name:
                    for entity in self.appProp:
                        print("entity[1]: ", entity[1])
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

            elif type_name == "amount":
                print("amount")
                if scene_name is None:
                    for entity in self.amtProp:
                        for items in entity[0]:
                            if items == prop_name:
                                return entity[0], entity[1]

                elif scene_name:
                    for entity in self.amtProp:
                        print("entity[1]: ", entity[1])
                        if entity[1] == scene_name:
                            return entity[0], entity[1]

        return None, None

    def queryAction(self, act_name, object_name, scene_name):
        # entity[0] = actions
        # entity[1] = object
        # entity[2] = scene

        if scene_name is None:
            for entity in self.act:
                for action in entity[0][1]:
                    if action == act_name:
                        return entity[0], entity[1], entity[2]

        elif act_name is None:
            for entity in self.act:
                if entity[2] == scene_name:
                    return entity[0], entity[1], entity[2]

        return None, None, None

