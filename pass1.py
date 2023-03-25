from sys import argv
from numpy import float32
from format import format_line


def read_general_data_statement(line):
    line = line.replace(';', '')
    data = line.split()
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
            data[0] = 7
        case 'SV2':
            data[0] = 8
        case 'PLF':
            #TODO
            print('Error: PlF not currently implemented.')
            return None
        case 'PLS':
            data[0] = 10
        case 'SI3':
            data[0] = 11
        case 'SIA':
            data[0] = 12
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
            #TODO
            data[0] = 110
            print("Error: SET not currently implemented.")
            return None
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
    output = ""
    in_instr_def = False
    
    for line in score_file:
        if not in_instr_def:
            next_output = read_general_data_statement(line)
            if next_output is not None and next_output[1] == 2:
                in_instr_def = True
                instr_start_time = next_output[2]
        else:
            next_output = read_instrument_data_statement(line, instr_start_time)
            if next_output == [2, 2, instr_start_time]: in_instr_def = False
        
        if next_output is not None:
            output += format_line(next_output)
    return output


def main():
    score_file = open(argv[1], "r")
    output = read_score(score_file)
    output_file = open("pass1.out", "w")
    output_file.write(output)


if __name__ == '__main__':
    main()