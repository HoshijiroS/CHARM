import model.dialogue_manager.content_provider as cont_plan


def parseWhoMessage(sequence, posList, ofList, toList, charList):
    output = []

    if [item for item in sequence if "VBZ" in item] or [item for item in sequence if "VBP" in item]:
        if posList:
            for index in posList:
                value = cont_plan.confirmCharacter(sequence[index - 1][0], 0, relationship=sequence[index + 1][0])

                if value not in output:
                    output.append(value)

        elif ofList:
            for index in ofList:
                value = cont_plan.confirmCharacter(sequence[index + 1][0], 0, relationship=sequence[index - 1][0])

                if value not in output:
                    output.append(value)

        elif toList:
            for index in toList:
                value = cont_plan.confirmCharacter(sequence[index + 1][0], 0, person=sequence[index - 1][0])

                if value not in output:
                    output.append(value)

        else:
            for character in charList:
                value = cont_plan.confirmCharacter(character, 0)

                if value not in output:
                    output.append(value)

    return output


def parseWhereMessage(charList, verbList):
    output = []

    if charList:
        if verbList:
            for character in charList:
                for action in verbList:
                    value = cont_plan.confirmCharacter(character, 1, action=action)

                    if value not in output:
                        output.append(value)

                    #output.append(cont_plan.confirmCharacter(character, 1, action=action))

    return output


def parseWhatMessage(sequence, posList, ofList, charList, andList, itemList, special=None):
    output = []

    if [item for item in sequence if "name" in item]:
        for index in posList:
            value = cont_plan.confirmCharacter(sequence[index - 1][0], 0, relationship=sequence[index + 1][0])

            if value not in output:
                output.append(value)

        for index in ofList:
            value = cont_plan.confirmCharacter(sequence[index + 1][0], 0, relationship=sequence[index - 1][0])

            if value not in output:
                output.append(value)

    elif [item for item in sequence if "relationship" in item]:
        for index in andList:
            value = cont_plan.confirmCharacter(sequence[index - 1][0], 0, person=sequence[index + 1][0])

            if value not in output:
                output.append(value)

    elif [item for item in sequence if "appearance" in item] or [item for item in sequence if "look" in item]:
        if special == "true":
            if itemList:
                for characters in charList:
                    if posList:
                        for index in posList:
                            value = cont_plan.confirmCharacter(characters, 2,
                                                               item=sequence[index + 1][0],
                                                               propType="appearance")

                            if value not in output:
                                output.append(value)

        else:
            if itemList:
                if posList:
                    for index in posList:
                        value = cont_plan.confirmCharacter(sequence[index - 1][0], 2, item=sequence[index + 1][0],
                                                                 propType="appearance")

                        if value not in output:
                            output.append(value)

                else:
                    for index in ofList:
                        value = cont_plan.confirmCharacter(sequence[index + 1][0], 2, item=sequence[index - 1][0],
                                                                 propType="appearance")

                        if value not in output:
                            output.append(value)

            else:
                try:
                    charList.remove("appearance")
                except Exception as e:
                    a = 1

                try:
                    charList.remove("look")
                except Exception as e:
                    a = 1

                for character in charList:
                    value = cont_plan.confirmCharacter(character, 2, propType="appearance")

                    if value not in output:
                        output.append(value)

    elif [item for item in sequence if "personality" in item] or [item for item in sequence if "like" in item]:
        try:
            charList.remove("personality")
        except Exception as e:
            a = 1

        try:
            charList.remove("like")
        except Exception as e:
            a = 1

        for character in charList:
            value = cont_plan.confirmCharacter(character, 2, propType="personality")

            if value not in output:
                output.append(value)

    elif [item for item in sequence if "meaning" in item] and [item for item in sequence if "of" in item]:
        output.append(cont_plan.generateMeaningForWord(sequence, word="end"))

    elif [item for item in sequence if "mean" in item]:
        output.append(cont_plan.generateMeaningForWord(sequence, word="mid"))

    return output


def parseWhyMessage(charList, objList, verbList, advList, itemList, adjList):
    output = []

    charList.extend(itemList)
    adjList.extend(advList)
    verbList.extend(adjList)

    for character in charList:
        #print("character: ", character)
        for action in verbList:
            #print("action: ", action)
            for obj in objList:
                #print("object: ", obj)
                if adjList:
                    for properties in adjList:
                        value = cont_plan.confirmCharacter(character, 3, action=action, item=obj, prop=properties)

                        if type(value) is list:
                            if value not in output:
                                output.extend(value)

                        else:
                            if value not in output:
                                output.append(value)

                else:
                    value = cont_plan.confirmCharacter(character, 3, action=action, item=obj)

                    if type(value) is list:
                        if value not in output:
                            output.extend(value)

                    else:
                        if value not in output:
                            output.append(value)

    #print("output: ", output)
    #output = list(set(output))

    return output
