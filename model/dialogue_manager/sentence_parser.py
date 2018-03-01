import model.dialogue_manager.content_provider as cont_plan


def parseWhoMessage(sequence, posList, ofList, toList, charList):
    if [item for item in sequence if "VBZ" in item] or [item for item in sequence if "VBP" in item]:
        if posList:
            for index in posList:
                return cont_plan.confirmCharacter(sequence[index - 1][0], 0, relationship=sequence[index + 1][0])

        elif ofList:
            for index in ofList:
                return cont_plan.confirmCharacter(sequence[index + 1][0], 0, relationship=sequence[index - 1][0])

        elif toList:
            for index in toList:
                return cont_plan.confirmCharacter(sequence[index + 1][0], 0, person=sequence[index - 1][0])

        else:
            for character in charList:
                return cont_plan.confirmCharacter(character, 0)


def parseWhereMessage(charList, verbList):
    if charList:
        if verbList:
            for character in charList:
                for action in verbList:
                    return cont_plan.confirmCharacter(character, 1, action=action)


def parseWhatMessage(sequence, posList, ofList, charList, andList, itemList):
    if [item for item in sequence if "name" in item]:
        for index in posList:
            return cont_plan.confirmCharacter(sequence[index - 1][0], 0, relationship=sequence[index + 1][0])

        for index in ofList:
            return cont_plan.confirmCharacter(sequence[index + 1][0], 0, relationship=sequence[index - 1][0])

    elif [item for item in sequence if "relationship" in item]:
        for index in andList:
            return cont_plan.confirmCharacter(sequence[index - 1][0], 0, person=sequence[index + 1][0])

    elif [item for item in sequence if "appearance" in item]:
        if itemList:
            if posList:
                for index in posList:
                    return cont_plan.confirmCharacter(sequence[index - 1][0], 2, item=sequence[index + 1][0],
                                                      propType="appearance")

            else:
                for index in ofList:
                    return cont_plan.confirmCharacter(sequence[index + 1][0], 2, item=sequence[index - 1][0],
                                                      propType="appearance")

        else:
            charList.remove("appearance")
            for character in charList:
                return cont_plan.confirmCharacter(character, 2, propType="appearance")

    elif [item for item in sequence if "personality" in item]:
        charList.remove("personality")
        for character in charList:
            return cont_plan.confirmCharacter(character, 2, propType="personality")


def parseWhyMessage(charList, verbList):
    for character in charList:
        for action in verbList:
            return cont_plan.confirmCharacter(character, 3, action=action)
