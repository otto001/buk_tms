import copy
import multiprocessing
from tm.turing_machine import TuringMachine, random_transition_dest
import random


keep = 0.1
gen_size = 500
tms = list()

def run_tm(tm):
    return tm.run()


if __name__ == "__main__":
    for i in range(gen_size):
        tm = TuringMachine()
        tm.randomize()
        tms.append(tm)

    tm = TuringMachine()
    tm.commands = tm.parse_file("tm_153.txt")
    tms.append(tm)

    for run in range(2000):
        with multiprocessing.Pool(6) as p:
            result = p.map(run_tm, tms)

        result = [x for x in result if x.accepted]
        result.sort(key=lambda tm: -tm.get_score())
        result = result[:int(keep*len(result))]

        if run % 10:
            print(result[0].get_score())
            result[0].write_to_file("tm_current.txt")

        tms = result

        for tm in tms:
            tm.reset()

        for _ in range(gen_size - len(tms)):
            tm: TuringMachine = random.choice(tms)

            commands = dict(tm.commands)
            transition_key = random.choice(list(commands.keys()))
            commands[transition_key] = random_transition_dest()

            tm = TuringMachine(commands, "")

            tms.append(tm)




















