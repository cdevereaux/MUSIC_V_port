from sys import argv
from format import format_line

G = [0]*1000

def sort_data_statements(input_file):
    lines = [line for line in input_file]
    #sort() is guarenteed to be stable, so no need to keep track of the indices of the lines
    lines.sort(key=lambda line: int(float(line.split()[2])))
    return [ [int(float(i)) for i in line.split()[:2]] + [float(i) for i in line.split()[2:]] for line in lines]


def main():
    global G

    input_file = open(argv[1], "r")
    data_statements = sort_data_statements(input_file)

    last_T = 0; last_B = 0
    for data in data_statements:
        match data[1:]:
            #SV2 or SIA
            case [8 | 12, action_time, starting_index, *values]:
                for i in range(len(values)):
                    G[int(starting_index)+i] = values[i]
            #PLS
            case [10, action_time, subroutine_num, *params]:
                call_PLS(data, G, data_statements)

        #Apply metronomic time scaling
        if G[1] != 0:
            B = data[2]
            i = 0
            while G[G[1] + 2*i] < B:
                i += 1
            tempo = G[G[1] + 2*i - 2] + (G[G[1] + 2*i] - G[G[1] + 2*i - 2])*(B - G[G[1] + 2*i - 1])/(G[G[1] + 2*i + 1] - G[G[1] + 2*i - 1]) 
            data[2] = last_T + (B - last_B)*(60/tempo)
            last_T = data[2]
            last_B = B

            if data[1] == 1:
                data[4] = data[4] * (60/tempo)
        

        #Implement CONVT
        CONVT(data, G)
    

    output_file = open("pass2.out", "w")

    output = [format_line(line) for line in data_statements]
    output = ''.join(output )
    output_file.write(output)


#Converts note freqs given in hertz
def CONVT(P, G):
    if G[100] != 5:
        return
    if P[1] == 1 and P[3] == 1:
        P[6] = 511.0 * P[6] / 44100
    return


def call_PLS(data, output, G, data_statements):
    P = data[:1]
    match int(data[2]):
        case 1:
            PLS1(P, G, data_statements)
        case 2:
            PLS2(P, G, data_statements)
        case 3:
            PLS3(P, G, data_statements)
        case 4:
            PLS4(P, G, data_statements)
        case 5:
            PLS5(P, G, data_statements)
        case _:
            raise ValueError(f"Unrecognized PLF subroutine called: PLF{data_statement[2]}")

def PLS1(P, G, data_statements):
    pass
def PLS2(P, G, data_statements):
    pass
def PLS3(P, G, data_statements):
    pass
def PLS4(P, G, data_statements):
    pass
def PLS5(P, G, data_statements):
    pass

if __name__ == '__main__':
    main()