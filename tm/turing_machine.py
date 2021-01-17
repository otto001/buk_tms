#!/usr/bin/env python

import random

symbols = ("0", "1", "_")
directions = ("l", "*", "r")

max_transitions = 50000


def random_transition_dest():
    return (random.choice(symbols),
            random.choice(directions),
            random.choice(["0", "1", "2", "3", "4", "halt"]))


class TuringMachine(object):
    counter = 0

    def __init__(self, commands=None, initial=""):
        self.commands = commands
        self.reset()

    def reset(self):
        self.tape = list(f"__")
        self.accepted = None
        self.place = 1
        self.state = "0"
        self.key = (self.state, self.tape[self.place])
        self.wild_key = (self.state, "*")

    def randomize(self):
        self.commands = dict()
        for current_q in range(5):
            for symbol in symbols:
                # t = (current_q, symbol, random.choice(symbols), random.choice(directions), random.randint(0, 4))
                self.commands[str(current_q), symbol] = random_transition_dest()

    def parse_file(self, filename):
        """Parse turing code from filename into a dict of commands."""
        with open(filename) as f:
            lines = map(str.strip, f.read().splitlines())
            lines = [line for line in lines if not line.startswith(';')]
            lines = map(lambda x: x.split(';')[0].strip().split(' '), lines)
            return dict([(tuple(i[:2]), tuple(i[2:])) for i in lines])

    def transitions_as_string(self):
        result = ""
        for key, dest in self.commands.items():
            result += " ".join([*key, *dest]) + "\n"
        return result

    def write_to_file(self, path):
        with open(path, "w") as file:
            file.write(self.transitions_as_string())

    def run(self):
        """Run the turing machine."""
        i = 0
        while (self.key in self.commands
               or self.wild_key in self.commands
               and not self.key[0].startswith("halt")):
            # Visualize initial state
            # Get things to do from hash table
            newchar, action, newstate = (self.commands.get(self.key)
                                         or self.commands[self.wild_key])
            self.tape[self.place] = (newchar
                                     if newchar != '*'
                                     else self.tape[self.place])

            # Update the tape accordingly
            if action == "l":
                self.place = self.place - 1
                if self.place == -1:  # Handle moving past beginning
                    self.tape.insert(0, "_")
                    self.place = 0
            elif action == "r":
                self.place = self.place + 1
                if self.place == len(self.tape):  # Handle moving past end
                    self.tape.append("_")

            # Update the current state/key/wild
            self.state = newstate
            self.key = (self.state, self.tape[self.place])
            self.wild_key = (self.state, '*')
            i += 1
            if i > max_transitions:
                self.accepted = False
                return self
        else:
            self.accepted = self.key[0].startswith("halt")
            return self

    def get_score(self):
        return self.tape.count("1")


if __name__ == "__main__":
    machine = TuringMachine(None, "")
    machine.randomize()
    machine.run()
