import model.Character as char
import model.Item as item
import model.Location as loc

# def generateAllchar.Characteracters():
students = char.Character("Students", ["Student", "Townsperson"])
girls = char.Character("girls", ["Student", "Townsperson"])
wanda = char.Character("Wanda", ["Student", "Townsperson"])
bill_byron = char.Character("Bill Byron", ["Student", "Townsperson"])
peggy = char.Character("Peggy", ["Student", "Townsperson"])
maddie = char.Character("Maddie", ["Student", "Townsperson"])
people = char.Character("townspeople", ["Townsperson"])
svenson = char.Character("Svenson", ["Townsperson"])
cecile = char.Character("Cecile", ["Student"])
miss_mason = char.Character("Miss Mason", ["Townsperson"])
jake_petronski = char.Character("Jake Petronski", ["Student", "Townsperson"])
jan_petronski = char.Character("Jan Petronski", ["Townsperson"])
jack_beggles = char.Character("Jack Beggles", ["Townsperson"])

# Wanda#
wanda.hasRelationship(jake_petronski.name, "brother")
wanda.hasRelationship(jan_petronski.name, "father")
wanda.hasRelationship(peggy.name, ["friend", "classmate"])
wanda.hasRelationship(maddie.name, ["friend", "classmate"])
wanda.hasRelationship(girls.name, "classmate")
wanda.hasRelationship(cecile.name, "classmate")
wanda.hasRelationship(students.name, "classmate")
wanda.hasRelationship(miss_mason.name, "teacher")
wanda.hasRelationship(svenson.name, "neighbor")
wanda.hasRelationship(bill_byron.name, "classmate")

# Maddie#
maddie.hasRelationship(peggy.name, ["best friend", "classmate"])
maddie.hasRelationship(wanda.name, ["friend", "classmate"])
maddie.hasRelationship(girls.name, "classmate")
maddie.hasRelationship(cecile.name, "classmate")
maddie.hasRelationship(students.name, "classmate")
maddie.hasRelationship(miss_mason.name, "teacher")
maddie.hasRelationship(bill_byron.name, "classmate")

# Peggy#
peggy.hasRelationship(maddie.name, ["best friend", "classmate"])
peggy.hasRelationship(wanda.name, ["friend", "classmate"])
peggy.hasRelationship(girls.name, "classmate")
peggy.hasRelationship(cecile.name, "classmate")
peggy.hasRelationship(students.name, "classmate")
peggy.hasRelationship(miss_mason.name, "teacher")
peggy.hasRelationship(bill_byron.name, "classmate")

# Cecile#
cecile.hasRelationship(maddie.name, ["friend", "classmate"])
cecile.hasRelationship(peggy.name, ["friend", "classmate"])
cecile.hasRelationship(girls.name, "classmate")
cecile.hasRelationship(wanda.name, "classmate")
cecile.hasRelationship(miss_mason.name, "teacher")
cecile.hasRelationship(students.name, "classmate")
cecile.hasRelationship(bill_byron.name, "classmate")

# Bill Byron#
bill_byron.hasRelationship(maddie.name, "classmate")
bill_byron.hasRelationship(peggy.name, "classmate")
bill_byron.hasRelationship(girls.name, "classmate")
bill_byron.hasRelationship(wanda.name, "classmate")
bill_byron.hasRelationship(students.name, "classmate")
bill_byron.hasRelationship(miss_mason.name, "teacher")

# Jack Beggles#
jack_beggles.hasRelationship(maddie.name, "classmate")
jack_beggles.hasRelationship(peggy.name, "classmate")
jack_beggles.hasRelationship(girls.name, "classmate")
jack_beggles.hasRelationship(wanda.name, "classmate")
jack_beggles.hasRelationship(students.name, "classmate")
jack_beggles.hasRelationship(miss_mason.name, "teacher")

# Svenson#
svenson.hasRelationship(wanda.name, "neighbor")
svenson.hasRelationship(people.name, "neighbor")

# Miss Mason#
miss_mason.hasRelationship(maddie.name, "student")
miss_mason.hasRelationship(peggy.name, "student")
miss_mason.hasRelationship(wanda.name, "student")
miss_mason.hasRelationship(girls.name, "student")
miss_mason.hasRelationship(students.name, "student")
miss_mason.hasRelationship(bill_byron.name, "student")
miss_mason.hasRelationship(jack_beggles.name, "student")

charList = {"students": students, "girls": girls, "wanda": wanda, "bill byron": bill_byron, "peggy": peggy,
                      "maddie": maddie, "people": people, "svenson": svenson, "cecile": cecile,
                      "miss mason": miss_mason,
                      "jake petronski": jake_petronski, "jan petronski": jan_petronski, "jack beggles": jack_beggles}

# def generateAllitem.Items():
friend = item.Item("friend")
grades = item.Item("grades")
shoes = item.Item("shoes")
clothes = item.Item("clothes")
mother = item.Item("mother")
name = item.Item("name")
dress = item.Item("dress")
game = item.Item("dresses game")
hun_dresses = item.Item("100 dresses")
note = item.Item("note")
contest = item.Item("drawing contest")
drawing = item.Item("drawing")
medal = item.Item("medal")
letter = item.Item("letter")
house = item.Item("house")
frame_house = item.Item("frame house")
friendly_letter = item.Item("friendly letter")

itemList = {"friend": friend, "shoes": shoes, "clothes": clothes, "mother": mother, "name": name, "dress": dress,
                 "game": game, "hun dresses": hun_dresses, "note": note, "drawing contest": contest, "drawing": drawing,
                 "medal": medal, "letter": letter, "house": house, "friendly letter": friendly_letter, "grades": grades, "frame house": frame_house}

# def generateAllloc.Locationations():
school = loc.Location("School")
rm13 = loc.Location("Room 13")
corner_of_room = loc.Location("corner of the room")
front_row = loc.Location("front row")
boggins_heights = loc.Location("Boggins Heights")
boggins_heights_road = item.Item("road")
neighborhood = loc.Location("neighborhood")
svenson_house = item.Item("Svenson's house")
oliver_street = loc.Location("Oliver Street")

locList = {"school": school, "rm13": rm13, "corner of room": corner_of_room, "front row": front_row,
                    "boggins heights": boggins_heights, "boggins heights road": boggins_heights_road,
                    "neighborhood": neighborhood, "svenson house": svenson_house,
                    "oliver street": oliver_street}