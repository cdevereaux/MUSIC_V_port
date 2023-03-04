from sys import argv


def sort_data_statements(input_file):
    lines = [line for line in input_file]
    #sort() is guarenteed to be stable, so no need to keep track of the indices of the lines
    lines.sort(key=lambda line: int(float(line.split()[2])))
    return ''.join(lines)


def main():
    input_file = open(argv[1], "r")
    output = sort_data_statements(input_file)
    #TODO: Handle SV2, SIA, and PLS
    #TODO: Apply metronomic time to opcodes listed on page 147
    output_file = open("pass2.out", "w")
    #TODO: Implement CONVT
    output_file.write(output)


if __name__ == '__main__':
    main()