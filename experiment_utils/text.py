
import numpy as np

def format_table(t, headers = None):

    if headers is None:
        if not len(t):
            return ''
        headers = [''] * len(t[0])

    max_widths = np.array([len(x) for x in headers])
    for row in t:
        max_widths = np.maximum(max_widths, [len(str(x)) for x in row])

    result = ''
    def produce_row(row, fill = ' '):
        nonlocal result
        sep = ' '
        result += sep.join(
            str(r) + fill * (m - len(str(r)))
            for r, m in zip(row, max_widths)
        ) + '\n'

    produce_row(headers)
    produce_row([''] * len(headers), fill = '-')
    for row in t:
        produce_row(row)

    return result


