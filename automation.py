import shutil

import numpy as np
import pandas as pd
import csv
import numpy
import os

move_idx = 0
index1 = 0
index2 = 0
index3 = 0
index4 = 0
index5 = 0

def index_update(line):
    global move_idx
    global index1
    global index2
    global index3
    global index4
    global index5
    move_idx = line.index('MOVE')
    index1 = line.index(' ', move_idx)
    index2 = line.index(' ', index1 + 1)
    index3 = line.index(' ', index2 + 1)
    index4 = line.index(' ', index3 + 1)
    #index5 = line.index(' ', index4 + 1)

trsfm = pd.read_csv('./Transformations.csv', header=None, index_col=None)
Data = np.array(trsfm)

format = '.pc'

try:
    os.rename('.\HeadImpactModel.pc', '.\HeadImpactModel.pc'[:-3] + '.txt')


except FileNotFoundError:
    print('input was already a txt file')

format = '.txt'
op = open('.\HeadImpactModel'+format, 'r', encoding='utf8')
op_text = op.read()

op.close()

for i, tp in enumerate(Data):
    original = r'D:\pedestrian\impact13_C.2.6.10\HeadImpactModel' + format
    target = r'D:\pedestrian\trsfms\HeadImpactModel' + f'_TP{i + 1}.txt'
    shutil.copyfile(original, target)
    with open(target, 'w', encoding='utf8') as tpf:
        x = 0
        for line in op_text.splitlines():
            if 'MOVE' in line:
                index_update(line)

                # print(str(line[index1 + 1:index2]))
                # print(str(line[index2 + 1:index3]))
                # print(str(line[index3 + 1:index4]))
                # print(str(line[index4 + 1:index5]))
                # print('')

                #print(move_idx, index1, index2)
                new_line = line.replace((str(line[index1+1:index2])), str(Data[i][9-x]))
                if x==0:
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index2 + 1:index3])), '0')
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index3 + 1:index4])), '0')
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index4 + 1:-1])), '1')

                elif x == 1:
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index2 + 1:index3])), '0')
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index3 + 1:index4])), '1')
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index4 + 1:-1])), '0')

                elif x == 2:
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index2 + 1:index3])), '1')
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index3 + 1:index4])), '0')
                    index_update(new_line)
                    new_line = new_line.replace((str(new_line[index4 + 1:])), '0')
                x += 1
                op_text = op_text.replace(line, new_line)
        tpf.write(op_text)
    try:

        os.rename(target, target[:target.index('.')] + '.pc')

    except FileNotFoundError:
        print('input was already a pc file')
try:

    os.rename('.\HeadImpactModel.txt', '.\HeadImpact.txt'[:-4] + '.pc')

except FileNotFoundError:
    print('input was already a pc file')
