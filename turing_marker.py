import json
import sys
from enum import Enum

class ComputationStatus(Enum):
    ACCEPTED = 1
    REJECTED = 0
    RUNNING = 2
    ERROR = -1

class TuringMachine:
    def __init__(self, states, lang_alphabet, tape_alphabet, transitions, accept_state, reject_state, initial_state):
        self.states = states
        self.lang_alphabet = lang_alphabet
        self.tape_alphabet = tape_alphabet
        self.alphabet = tape_alphabet + lang_alphabet 
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_state = accept_state
        self.reject_state = reject_state

class TuringMachineComputation:
    def __init__(self, machine: TuringMachine, input_string: str):
        self.machine = machine
        self.input_string = input_string

        self.head = 0
        self.state = self.machine.initial_state
        self.tape = [ self.machine.alphabet.index(symbol) for symbol in input_string ]

        self.status = ComputationStatus.RUNNING

    def step(self):
        if (self.status != ComputationStatus.RUNNING):
            return

        for trans in self.machine.transitions:
            if trans[0] == self.state and trans[1] == self.tape[self.head]:
                current_transition = trans

        if (not current_transition):
            self.status = ComputationStatus.ERROR
            return

        self.tape[self.head] = current_transition[3]
        self.head += current_transition[4]
        self.state = current_transition[2]

        if self.head + current_transition[4] >= len(self.tape):
            self.tape = self.tape + [ 0 for _ in range(len(self.tape)) ]

        if self.head + current_transition[4] < 0:
            self.tape = [ 0 for _ in range(len(self.tape))] + self.tape
            self.head = len(self.tape) + current_transition[4]


        if (current_transition[2] == self.machine.accept_state):
            self.status = ComputationStatus.ACCEPTED

        if (current_transition[2] == self.machine.reject_state):
            self.status = ComputationStatus.REJECTED

    def step_until_halt(self, max_steps = 1_000_000):
        for _ in range(max_steps):
            if self.status == ComputationStatus.REJECTED or self.status == ComputationStatus.ACCEPTED:
                break

            self.step()

class TuringMachineFile:
    def __init__(self, identifier, machine, _diagram, computations):
        self.identifier = identifier
        self.machine = machine
        self.diagram = _diagram
        self.computations = computations

    def from_json(json_tm_file):
        data = json.loads(json_tm_file)
        return TuringMachineFile(
            data['identifier'],
            TuringMachine(
                data['machine']['states'],
                data['machine']['lang_alphabet'],
                data['machine']['tape_alphabet'],
                data['machine']['transitions'],
                data['machine']['accept_state'],
                data['machine']['reject_state'],
                data['machine']['initial_state'],
            ),
            data['diagram'],
            data['computations']
        )

def eprint(message):
    print(message, file=sys.stderr)

def main():
    if len(sys.argv) != 2:
        eprint("Incorrect Arguments: Specify JSON Turing Machine filepath")
        exit(-1)

    json_tm_filepath = str(sys.argv[1])
    test_case = str(input())

    with open(json_tm_filepath, 'r', encoding='utf-8') as f:
        json_tm_file = f.read()
        tm_file = TuringMachineFile.from_json(json_tm_file)

    if test_case == "":
        test_case = tm_file.machine.alphabet[0]

    computation = TuringMachineComputation(tm_file.machine, test_case)
    computation.step_until_halt()
    print(computation.status.value)

if __name__ == "__main__":
    main()