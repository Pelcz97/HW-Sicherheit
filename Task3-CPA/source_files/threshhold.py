#!/usr/bin/env python3
import csv
import numpy as np
import sys


def main():
    if len(sys.argv) != 3:
        print('Usage: program [traces.csv] [output_dir]')
        sys.exit(0)

    traces = np.genfromtxt(sys.argv[1], dtype=int, delimiter=',')
    min_value = np.min(traces[np.nonzero(traces)])
    max_value = traces.max()
    # print(f'Values in traces range from {min_value} to {max_value}.')

    file_basename = sys.argv[2].replace('/', '') + sys.argv[1][sys.argv[1].find('/'):-4] + '_'
    for threshold in range(int(min_value), int(max_value)):
        threshold_traces = np.where(traces <= threshold, 0, 1)
        filename = file_basename + str(threshold) + '.csv'
        path = sys.argv[2] + filename
        np.savetxt(path, threshold_traces, fmt="%d", delimiter=",")
        # print(f'Saved traces for threshold {threshold} to {filename}')


if __name__ == '__main__':
    main()
