from sys import argv
from imposterlist import imposter_list
from numpy import array, float32

SAMPLING_RATE = 44100
FUNCTION_LEN = 512
IO_BLOCK_LEN = 512
IO_OUTPUT_BLOCK = 1

#See p. 160
# IP(1) = NUMBER OF OP CODES
# IP(2) = BEGINNING SUBSCRIPT OF FIRST FUNCTION
# IP(3) = STANDARD SAMPLING RATE
# IP(4) = BEGINNING SUBSCRIPT OF INSTRUMENT DEFINITIONS
# IP(5) = BEGINNING OF LOCATION TABLE FOR INSTRUMENT DEFINITIONS
# IP(6) = LENGTH OF FUNCTIONS
# IP(7) = BEGINNING OF NOTE CARD PARAMETERS
# IP(8) = LENGTH OF NOTE CARD PARAMETER BLOCKS
# IP(9) = NUMBER OF NOTE CARD PARAMETER BLOCKS
# IP(10) = BEGINNING OF OUTPUT DATA BLOCK
# IP(11) = SOUND ZERO (SILENCE VALUE)
# IP(12) = SCALE FACTOR FOR NOTE CARD PARAMETERS
# IP(13) = BEGINNING OF GENERATOR INPUT-OUTPUT BLOCKS
# IP(14) = LENGTH OF GENERATOR INPUT-OUTPUT BLOCKS
# IP(15) = SCALE FACTOR FOR FUNCTIONS
IP = [12, 512, 44100, 14500, 14400, 512, 13000, 35, 40, 6657, 
      2048, 1000000, 6657, 512, 7777777, 0, 0, 0, 0, 0, 0]

Integers = dict()
Variables = dict()
Instruments = dict()
Functions = dict()
Note_Parameters = list()
IO_Blocks = dict()

def read_general_data_statement(line):
    data = [float(word) for word in line.split()][1:]
    data[0] = int(data[0])
    return data

def process_general_data_statement(file, data):
    global Note_Parameters
    global Functions
    
    print(data)
    match data:
        #NOT
        case [1, action_time, instrument_number, *other_parameters]:
            note = [int(instrument_number), action_time, instrument_number, *other_parameters]
            note += [0]*(100 - len(note))
            Note_Parameters.append(note)
            return (1, action_time)
        #INS
        case [2, action_time, instrument_number]:
            construct_instrument(file, instrument_number)
            return (2, action_time)
        #GEN
        case [3, action_time, gen_subroutine, fun_num, *other_parameters]:
            fun = generate_function(gen_subroutine, *other_parameters)
            print(fun)
            print(len(fun))
            Functions[fun_num] = fun
            return (3, action_time)
        #SV3
        case [4, action_time, starting_index, *values]:
            for i in range(len(values)):
                Variables[starting_index+i] = values[i]
        #SEC
        case [5, action_time]:
            #TODO
            return (5, action_time)
        #TER
        case [6, action_time]:
            #TODO: wait until action_time, then terminate
            return (6, action_time)
        #SV1
        case [7, action_time, starting_index, *values]:
            print(f"Ignoring SV1 command: {data}")
        #SV2
        case [8, action_time, starting_index, *values]:
            print(f"Ignoring SV2 command: {data}")
        #PLF
        case [9, action_time, subroutine_num, *params]:
            print(f"Ignoring PLF command: {data}")
        #PLS
        case [10, action_time, subroutine_num, *params]:
            print(f"Ignoring PLS command: {data}")
        #SI3 or SIA
        case [11 | 12, action_time, starting_index, *values]:
            #TODO
            for i in range(len(values)):
                #See pg. 159 for list of special integers
                #TODO: process changes for special integers
                Variables[starting_index+i] = values[i]
        case other:
            print(f"Unknown general opcode: {data[0]}")


#Note: in the original program the old definitions of instruments are left in place
#in this implementation they are overwritten
def construct_instrument(file, instrument_number):
    global Instruments

    Instruments[instrument_number] = list()
    for line in file:
        data = [float(word) for word in line.split()][1:]
        if len(data) == 2:
            #Encountered END statement
            return
        data = data[2:]
        data[0] = int(data[0])
        Instruments[instrument_number].append(data)
    raise Exception(f"Encountered unexpected EOF while reading definition of instrument {instrument_number}")


def interpret_unit_gen_param(x, note):
    global IO_Blocks
    global Variables
    global Functions
    
    match int(x):
        case x if x < -100:
            if -x - 100 not in Functions:
                Functions[-x - 100] = [0]*FUNCTION_LEN
            return Functions[-x - 100]
        case x if x < 0:
            if -x not in IO_Blocks:
                IO_Blocks[-x] = [0]*IO_BLOCK_LEN
            return IO_Blocks[-x]
        case x if x == 0:
            raise ValueError("Zero Encountered in Unit Generator Definition.")
        case x if x < 101:
            return imposter_list(note, x-1)
        case x if x > 100:
            return imposter_list(Variables, x-100)
        

def play_note(note, duration):
    assert(duration <= IO_BLOCK_LEN)
    
    #Undefined instrument
    if note[0] not in Instruments:
        return

    for unit_generator in Instruments[note[0]]:
        match unit_generator:
            #OUT
            case [101, I, O]:
                I = interpret_unit_gen_param(I, note)
                O = interpret_unit_gen_param(O, note)
                
                for i in range(duration):
                    O[i] += I[i]
            #OSC
            case [102, I1, I2, O, F, S]:
                #print(unit_generator)
                I1 = interpret_unit_gen_param(I1, note)
                I2 = interpret_unit_gen_param(I2, note)
                O = interpret_unit_gen_param(O, note)
                F = interpret_unit_gen_param(F, note)
                S = interpret_unit_gen_param(S, note)
                for i in range(duration):
                    #print(I1[i], F[int(S[i]) % len(F)])
                    O[i] = (I1[i]/2048) * F[int(S[i]) % len(F)]
                    S[i+1] = S[i] + I2[i]
            #AD2
            case [103, I1, I2, O]:
                I1 = interpret_unit_gen_param(I1, note)
                I2 = interpret_unit_gen_param(I2, note)
                O = interpret_unit_gen_param(O, note)
                for i in range(duration):
                    O[i] = I1[i] + I2[i]
            #RAN
            case [104, I1, I2, O, S, T1, T2]:
                #TODO
                raise Exception('RAN not yet implemented')
            #ENV
            case [105, I1, F, O, I2, I3, I4, S]:
                #TODO
                raise Exception('ENV not yet implemented')
            #STR
            case 'STR':
                data[0] = 106
            #AD3
            case [107, I1, I2, I3, O]:
                I1 = interpret_unit_gen_param(I1, note)
                I2 = interpret_unit_gen_param(I2, note)
                I3 = interpret_unit_gen_param(I3, note)
                O = interpret_unit_gen_param(O, note)
                for i in range(duration):
                    O[i] = I1[i] + I2[i] + I3[i]
            #AD4
            case [108, I1, I2, I3, I4, O]:
                I1 = interpret_unit_gen_param(I1, note)
                I2 = interpret_unit_gen_param(I2, note)
                I3 = interpret_unit_gen_param(I3, note)
                I4 = interpret_unit_gen_param(I4, note)
                O = interpret_unit_gen_param(O, note)
                for i in range(duration):
                    O[i] = I1[i] + I2[i] + I3[3] + I4[i]
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
            case other:
                print(f"Unknown Unit Generator: {note}")


def generate_raw_audio(file):
    global Note_Parameters
    global IO_Blocks

    output = []
    played_to = 0
    for line in file:
    
        data = read_general_data_statement(line)
        play_to = data[1]

        while played_to < play_to:
            #print(played_to)
            stop_time = play_to
            for note in Note_Parameters:
                #action time + duration
                if note[1] + note[3] < stop_time:
                    stop_time = note[1] + note[3]
            #generate audio
            while played_to < stop_time:
                #print(played_to)
                IO_Blocks[IO_OUTPUT_BLOCK] = [0]*IO_BLOCK_LEN
                duration = int(min(1+(stop_time - played_to)*SAMPLING_RATE, IO_BLOCK_LEN))
                for note in Note_Parameters:
                    play_note(note, duration)
                output += IO_Blocks[IO_OUTPUT_BLOCK][:duration]
                played_to += duration/SAMPLING_RATE
            #remove any old notes
            Note_Parameters = [note for note in Note_Parameters if note[1] + note[3] > played_to]
        
        #TODO: Check for TER
        process_general_data_statement(file, data)
    
    return output


def main():
    input_file = open(argv[1], "r")
    samples = generate_raw_audio(input_file)
    output_file = open("audio.raw", "wb")
    float_array = array(samples, float32)
    output_file.write(float_array.tobytes())
    output_file.close()


def generate_function(gen_subroutine, *params):
    import gen
    match gen_subroutine:
        case 1:
            return gen.GEN1(params)
        case 2:
            return gen.GEN2(params, FUNCTION_LEN)
        case 3:
            return gen.GEN3(params, FUNCTION_LEN)
        case other:
            raise Exception(f"Unknown function generator: GEN{gen_subroutine}")


if __name__ == '__main__':
    main()