from sys import argv
from numpy import float32
from format import format_line

# A general storage array used by PLF subroutines
D = [0]*2000


def read_general_data_statement(line, output):
    line = line.replace(';', '')
    data = line.split()
    if len(data) == 0: return
    match data[0][:3]:
        case 'NOT':
            data[0] = 1
        case 'INS':
            data[0] = 2
        case 'GEN':
            data[0] = 3
        case 'SV3':
            data[0] = 4
        case 'SEC':
            data[0] = 5
        case 'TER':
            data[0] = 6
        case 'SV1':
            n = int(data[2])
            vars = data[3:]
            for i in range(len(vars)):
                D[n+i] = float(vars[i])
            return
        case 'SV2':
            data[0] = 8
        case 'PLF':
            call_PLF(data, output, D)
            return None
        case 'PLS':
            data[0] = 10
        case 'SI3':
            data[0] = 11
        case 'SIA':
            data[0] = 12
            n = int(data[2])
            vars = data[3:]
            for i in range(len(vars)):
                D[n+i] = float(vars[i])
        case 'COM':
            print(line)
            return None
        case other:
            print(f"Unknown general opcode: {data[0]}")
    return [len(data)] + data


def read_instrument_data_statement(line, time):
    line = line.replace(';', '')
    data = line.split()
    #Uses the type numbers from pass1.f, not from the manual
    match data[0][:3]:
        case 'OUT':
            data[0] = 101
        case 'OSC':
            data[0] = 102
        case 'AD2':
            data[0] = 103
        case 'RAN':
            data[0] = 104
        case 'ENV':
            data[0] = 105
        case 'STR':
            data[0] = 106
        case 'AD3':
            data[0] = 107
        case 'AD4':
            data[0] = 108
        case 'MLT':
            data[0] = 109
        case 'FLT':
            data[0] = 112
        case 'RAH':
            data[0] = 111
        case 'IOS':
            data[0] = 113
        case 'SET':
            data[0] = 110
        case 'COM':
            print(line)
            return None
        case 'END':
            return [2, 2, time]
        case other:
            print(f"Unknown instrument opcode: {data[0]}")
            return None
    
    data = [2, time] + data
    return [len(data)] + data


def read_score(score_file):
    output = []
    in_instr_def = False
    
    for line in score_file:
        if not in_instr_def:
            next_output = read_general_data_statement(line, output)
            if next_output is not None and next_output[1] == 2:
                in_instr_def = True
                instr_start_time = next_output[2]
        else:
            next_output = read_instrument_data_statement(line, instr_start_time)
            if next_output == [2, 2, instr_start_time]: in_instr_def = False
        
        if next_output is not None:
            output.append(format_line(next_output))
    return ''.join(output)

def main():
    score_file = open(argv[1], "r")
    output = read_score(score_file)
    output_file = open("pass1.out", "w")
    output_file.write(output)


def call_PLF(data_statement, output, D):
    P = data_statement[:1] + [float(datum) for datum in data_statement[1:]]
    match int(data_statement[2]):
        case 1:
            PLF1(P, D, output)
        case 2:
            PLF2(P, D, output)
        case 3:
            PLF3(P, D, output)
        case 4:
            PLF4(P, D, output)
        case 5:
            PLF5(P, D, output)
        case _:
            raise ValueError(f"Unrecognized PLF subroutine called: PLF{data_statement[2]}")

def PLF1(P, D, output):
    #from page 82 of Technology of Computer Music
    ns = P[3]
    ne = P[4]
    ts = P[5]
    ds = P[6]
    fs = P[7]
    P[0] = 1
    P[2] = P[8]
    P = P[:7]
    for i in range(int(ns), int(ne), 10):
        P[1] = ts + ds * D[i]
        P[3] = ds * D[i+1]
        P[4] = D[i+2]
        P[5] = (2**(D[i+3] + fs)) * 262
        output.append(format_line([len(P)] + P))
    return
    

def PLF2(P, D, output):
    pass
def PLF3(P, D, output):
    pass
def PLF4(P, D, output):
    pass
def PLF5(P, D, output):
    pass



if __name__ == '__main__':
    main()