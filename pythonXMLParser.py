import xml.etree.ElementTree as ET
import ast

tree = ET.parse('ArmyFirstAidOrganized.xml')

root = tree.getroot()

print("\n\nWhat kind of emergency?\n\n")


i = 1

for thing in root.iter('Type'):
    print(str(i) + "      " + thing[0].text + "\n")
    i +=1

num = int(input("Enter the corresponding number: "))


print("Do you know what kind of bite?")

i = 1

for thing in root[num-1].iter('Subtype'):
    print(str(i) +  "     " + thing[0].text + "\n")
    i += 1

num = int(input("Enter the corresponding number: "))

print("Here is the currently recommended treatment. Press enter key to continue to next step")

x = ast.literal_eval(root[0][3][3].text)

# print (root[0][3][3].text)


for thing in x:
    print(thing + "\n")
    blah = input("")

