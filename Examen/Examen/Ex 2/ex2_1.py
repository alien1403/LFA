# Echipa: Ignat Eduardo, Neagu Marian-Madalin

# functie care returneaza o lista cu elementele corespunzatoare
# fiecarei sectiuni
# functia primeste numele sectiunii asa cum apare in config file si o lista
def get_section(name, list_):
    ok = False
    list_section = []
    for line in list_:
        if line == name + ":":
            ok = True
            continue
        if line == "End":
            ok = False
        if ok:
            list_section.append(line)
    return list_section


# functia returneaza un 5 tuplu in care sunt stocate liste corespunzatoare
# cu valorile fiecarei sectiuni.
# Observatie: nu este 7 tuplu, deoarece am convenit sa stocam 'starea de start',
# 'starea de acceptare' si 'starea de reject' in aceeasi lista
def load_tm(file_name):
    list_ = []
    file = open(file_name)

    for line in file:
        line = line.strip()
        # ignoram simbolurile '#' pentru a pune comentarii cu ajutorul lor
        if len(line) > 0 and line[0] != "#":
            list_.append(line)

    list_states = get_section("States", list_)
    list_input_alphabet = get_section("Input alphabet", list_)
    list_tape_alphabet = get_section("Tape alphabet", list_)
    list_transitions_temp = get_section("Transitions", list_)
    list_start_accept_reject_states = get_section("Start state", list_) + get_section("Accept state", list_) + \
                                      get_section("Reject state", list_)
    # pentru a separa fiecare element din fiecare tranzitie am folosit o variabila temporara
    list_transitions = []
    for elem in list_transitions_temp:
        list_transitions.append(elem.split())

    return list_states, list_input_alphabet, list_tape_alphabet, list_transitions, list_start_accept_reject_states


# functia care valideaza fisierul de config pentru TM
# returneaza True daca este validat si Fals daca nu este acceptat
def validate(states, input_alphabet, tape_alphabet, transitions, start_accept_reject_states):
    # prima conditie este ca fiecare sectiune din fisier sa aibe elemente
    if len(states) < 1 or len(input_alphabet) < 1 or len(tape_alphabet) < 1 or len(transitions) < 1 or len(
            start_accept_reject_states) < 1:
        return False

    # urmatoarele conditii verifica daca:
    # - fiecare tranzitie din sectiunea Transitions are 8 elemente si anume (in ordine):
    #           - starea curenta
    #           - starea urmatoare
    #           - caracterul curent la care este capatul care porneste de la inceputul stringului
    #           - caracterul cu care va fi inlocuit caracterul curent la care este capatul mentionat anterior
    #           - directia in care se va deplasa capatul mentionat anterior
    #           - caracterul curent la care este capatul care porneste de la sfarsitul stringului
    #           - caracterul cu care va fi inlocuit caracterul curent la care este capatul mentionat anterior
    #           - directia in care se va deplasa capatul mentionat anterior
    # - fiecare stare (si cea curenta si urmatoarea) exista in multimea de stari
    # - fiecare caracter apartine alfabetului tape
    # - fiecare directie este valida (poate fi R - pentru dreapta, L - pentru stanga, sau N - pentru a
    # ramane in pozitia curenta)
    for transition in transitions:
        if len(transition) != 8:
            return False
        if transition[0] not in states or transition[1] not in states:
            return False
        if transition[2] not in tape_alphabet or transition[3] not in tape_alphabet or \
                transition[5] not in tape_alphabet or transition[6] not in tape_alphabet:
            return False
        if transition[4] not in ['R', 'L', 'N'] or transition[7] not in ['R', 'L', 'N']:
            return False

    # ultima conditie de validare este ca starile de start, acceptare si reject sa se regaseasca
    # in multimea de stari
    for elem in start_accept_reject_states:
        if elem not in states:
            return False

    return True

# despachetare tuplu in mai multe liste
states, input_alphabet, tape_alphabet, transitions, start_accept_reject_states = load_tm("ex2_1_exemplu.txt")
# bool in care se verifica daca TM este valid
valid = validate(states, input_alphabet, tape_alphabet, transitions, start_accept_reject_states)

if valid:
    print("TM is valid!")
else:
    print("TM is not valid!")
