from numpy import float32
from math import log10, floor


def format_line(data):
    out_str = "{:>12d}".format(data[0])

    for i in range(1, len(data)):
        if not (isinstance(data[i], int) or isinstance(data[i], float)):
            match data[i][0]:
                case 'P':
                    data[i] = float(data[i][1:])
                case 'V':
                    data[i] = 100 + float(data[i][1:])
                case 'F':
                    data[i] = -( 100 + float(data[i][1:]) )
                case 'B':
                    data[i] = -float(data[i][1:])
                case other:
                    data[i] = float(data[i])
        fmt_str = '{' + ':^ ' + ('17' if i != 1 else '16') + '.' + str(8  - (0 if data[i] == 0 else floor(log10(abs(data[i]))) ) ) + 'f' + '}'
        out_str += fmt_str.format(float32(data[i]))
    
    return out_str + ' \n'