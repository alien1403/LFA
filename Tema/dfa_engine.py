import sys

if len(sys.argv) < 2:
    print("Not enough arguments!")
    quit()

dfa_config = open(sys.argv[1], "r")

alphabet = set()
states = dict()
transitions = []

inSigma = False
inStates = False
inTransitions = False

for line in open("dfa_config.txt"):
    li = line.strip()
    if not li.startswith("#"):
        if li.upper() == "SIGMA:":
            inSigma = True

        if li.upper() == "STATES:":
            inStates = True

        if li.upper() == "TRANSITIONS:":
            inTransitions = True

        if li.upper() == "END":
            inSigma = False
            inStates = False
            inTransitions = False

        # adaugare litere in multime
        if inSigma and li.isalpha():
            alphabet.add(li)

        # adaugare stari in dictionar
        elif inStates and li != "" and li.upper() != "STATES:":
            li_temp = li.split(",")

            if len(li_temp) == 1:
                states.update({li_temp[0]: ""})
            elif len(li_temp) == 2:
                states.update({li_temp[0]: li_temp[1]})
            else:
                states.update({li_temp[0]: ('S', 'F')})

        elif inTransitions and li != "" and li.upper() != "TRANSITIONS:":
            transitions.append(li.split(","))


dfa_accepted = True

for lists in transitions:
    if not lists[0] in states or not lists[2] in states or not lists[1] in alphabet:
        dfa_accepted = False

if dfa_accepted:
    print("DFA accepted!")
else:
    print("DFA not accepted!")


