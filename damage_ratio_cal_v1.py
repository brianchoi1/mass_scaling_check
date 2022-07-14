from numpy import abs
from numpy import zeros
from numpy import array
# from time import time
from os import path
from re import findall

def curve_extract(fname):
    data = open(fname).readlines()      #fname = 'D:/LGE/1.1 work_others/damage_ratio/new_ver4/17'
    start = 0
    end = 0
    offset1 = 0
    offset2 = 20
    col1 = []
    col2 = []
    for i, line in enumerate(data):
        line = line.lower()
        if '* maxval' in line:
            start = i+1
        if 'endcurve' in line:
            end = i
            # id = str(data[start - 3]).split(' ')    
        for ii in range(start, end):
            col1.append(float(data[ii][offset1:offset2].replace(" ", "")))
            col2.append(float(data[ii][offset1+20:offset2+20].replace(" ", "")))
    return col1, col2

def dyna_parsing1(upper_fname, lower_fname, aaa, bbb, uts, fre, tt, bin): #fr : frequency list
    upper_total_dmg_list = []
    lower_total_dmg_list = []
    for fr, fn, lvv in zip(fre, upper_fname, range(int(bin))):
        lv = str(lvv + 1)
        dirr, file = path.split(fn)
        col1, col2 = curve_extract(fn)
        num = len(col1)
        B, sum_val = rainflow_core(dirr, col2, num, aaa, bbb, uts, lv, float(fr))
        upper_total_dmg_list.append(sum_val)
        upper_lv_total_dmg_list = sum(upper_total_dmg_list) * 6 * tt
    for fr, fn, lvv in zip(fre, lower_fname, range(int(bin))):
        lv = str(lvv + 1)
        dirr, file = path.split(fn)
        col1, col2 = curve_extract(fn)
        num = len(col1)
        B, sum_val = rainflow_core(dirr, col2, num, aaa, bbb, uts, lv, float(fr))
        lower_total_dmg_list.append(sum_val)
        lower_lv_total_dmg_list = sum(lower_total_dmg_list) * 6 * tt
    if upper_lv_total_dmg_list > lower_lv_total_dmg_list:
        return upper_lv_total_dmg_list
    elif upper_lv_total_dmg_list < lower_lv_total_dmg_list:
        return lower_lv_total_dmg_list
    else:
        return upper_lv_total_dmg_list

def dyna_parsing2(fname, aaa, bbb, uts, fre, tt, bin): #fr : frequency list
    total_dmg_list = []
    for fr, fn, lvv in zip(fre, fname, range(int(bin))):
        lv = str(lvv + 1)
        dirr, file = path.split(fn)
        col1, col2 = curve_extract(fn)
        num = len(col1)
        B, sum_val = rainflow_core(dirr, col2, num, aaa, bbb, uts, lv, float(fr))
        total_dmg_list.append(sum_val)
        lv_total_dmg_list = sum(total_dmg_list) * 6 * tt
    return lv_total_dmg_list

def col_collect(fname):
    open_fname = open(fname)
    data = open_fname.read()
    data = findall(r"[\S]+", data)
    data = list(map(float, data))
    col1 = data[0::2]
    col2 = data[1::2]
    return col1, col2

def float_sum(sum_damage):
    iii = 0
    for ii in sum_damage:
        iii += ii
    return iii

def damage_calculator(cycle,am,mv,mp,aaa,bbb,uts,fr):
    mean_stress = float(uts)*(((float(mp)-float(mv))/2)/(float(uts)-float(am)))
    if mean_stress == 0:
        damage = 0
    else:
        life_cycle = (mean_stress/float(aaa))**(-1/float(bbb))
        damage = (cycle*fr)/life_cycle
    return float(damage)

def rainflow_core(dirr, b,num,aaa,bbb,uts,lv,fr):
    # t0 = time()
    b = array(b)
    y = zeros(num, 'f')
    a = zeros(num, 'f')
    B = zeros((num, 4), 'f')
    y = b
    k = 0
    a[0] = y[0]
    k = 1
    for i in range(1, (num - 1)):

        slope1 = (y[i] - y[i - 1])
        slope2 = (y[i + 1] - y[i])

        if ((slope1 * slope2) <= 0):
            a[k] = y[i]
            k += 1
    last_a = k
    hold = last_a
    a[k] = y[num - 1]
    mina = min(a)
    maxa = max(a)
    nmm = int(maxa - mina) + 1
    n = 0
    i = 0
    j = 1
    summ = 0
    kv = 0
    ymax = -1.0e+20
    aa = a.tolist()
    nkv = 0
    ijk = 0
    LLL = int(0.2 * float(hold / 2))
    while (1):
        Y = abs(aa[i] - aa[i + 1])
        X = abs(aa[j] - aa[j + 1])
        if (X >= Y and Y > 0):
            if (Y > ymax):
                ymax = Y
            if (i == 0):
                n = 0
                summ += 0.5
                B[kv][3] = aa[i + 1]
                B[kv][2] = aa[i]
                B[kv][1] = 0.5
                B[kv][0] = Y
                kv += 1
                aa.pop(i)
                last_a -= 1
                i = 0
                j = 1
            else:
                summ += 1
                B[kv][3] = aa[i + 1]
                B[kv][2] = aa[i]
                B[kv][1] = 1.
                B[kv][0] = Y
                kv += 1
                n = 0
                aa.pop(i + 1)
                aa.pop(i)
                i = 0
                j = 1
                last_a -= 2
                nkv += 1
                ijk += 1
                if (ijk == LLL):
                    pr = (summ / (hold / 2)) * 100.
                    ijk = 0
        else:
            i += 1
            j += 1
        if ((j + 1) > last_a):
            break
    for i in range(0, last_a):
        Y = (abs(aa[i] - aa[i + 1]))
        if (Y > 0):
            summ += 0.5
            B[kv][3] = aa[i + 1]
            B[kv][2] = aa[i]
            B[kv][1] = 0.5
            B[kv][0] = Y
            kv += 1
            if (Y > ymax):
                ymax = Y
    sum_val = rainflow_bins(dirr, B, kv, hold, summ, ymax, num, aaa, bbb, uts, lv, fr)
    return B, sum_val

def rainflow_bins(dirr, B, kv, hold, summ, ymax, num,aaa,bbb,uts,lv,fr):
    L = zeros(18, 'f')
    C = zeros(18, 'f')
    AverageMean = zeros(18, 'f')
    MaxPeak = zeros(18, 'f')
    MinValley = zeros(18, 'f')
    MaxAmp = zeros(18, 'f')
    AverageAmp = zeros(18, 'f')

    L[1] = 0
    L[2] = 6.3
    L[3] = 12.5
    L[4] = 18.8
    L[5] = 25
    L[6] = 31.3
    L[7] = 37.5
    L[8] = 43.8
    L[9] = 50
    L[10] = 56.3
    L[11] = 62.5
    L[12] = 68.8
    L[13] = 75
    L[14] = 81.3
    L[15] = 87.5
    L[16] = 93.8
    L[17] = 100

    for ijk in range(1, 18):
        L[ijk] *= ymax / 100.
        MaxPeak[ijk] = -1.0e+20
        MinValley[ijk] = 1.0e+20
        MaxAmp[ijk] = -1.0e+20
    kv -= 1
    for i in range(0, kv + 1):
        Y = B[i][0]
        for ijk in range(16, 0, -1):
            if (Y >= L[ijk] and Y <= L[ijk + 1]):
                C[ijk] += B[i][1]
                AverageMean[ijk] += B[i][1] * (B[i][3] + B[i][2]) * 0.5  # weighted average
                if (B[i][3] > MaxPeak[ijk]):
                    MaxPeak[ijk] = B[i][3]
                if (B[i][2] > MaxPeak[ijk]):
                    MaxPeak[ijk] = B[i][2]
                if (B[i][3] < MinValley[ijk]):
                    MinValley[ijk] = B[i][3]
                if (B[i][2] < MinValley[ijk]):
                    MinValley[ijk] = B[i][2]
                if (Y > MaxAmp[ijk]):
                    MaxAmp[ijk] = Y
                AverageAmp[ijk] += B[i][1] * Y * 0.5
                break
    for ijk in range(1, 18):
        if (C[ijk] > 0):
            AverageMean[ijk] /= C[ijk]
            AverageAmp[ijk] /= C[ijk]
        if (C[ijk] < 0.5):
            AverageMean[ijk] = 0.
            AverageAmp[ijk] = 0.
            MaxPeak[ijk] = 0.
            MinValley[ijk] = 0.
            MaxAmp[ijk] = 0.
        MaxAmp[ijk] /= 2.
    outfile = open(dirr + '\\' + 'rainflow_counting_result.txt', "a")
    outfile.write('\n  Amplitude = (peak-valley)/2 \n\n')
    outfile.write('\n  Level: ' + str(lv) + '\n\n')
    outfile.write("          Range            Cycle       Ave      Max     Ave     Min       Max \n")
    outfile.write("         (units)           Counts      Amp      Amp     Mean    Valley    Peak \n")

    sum_damage = []
    for i in range(16, 0, -1):
        cycle = C[i]
        am = AverageMean[i]
        mv = MinValley[i]
        mp = MaxPeak[i]
        sum_damage.append(damage_calculator(cycle,am,mv,mp,aaa,bbb,uts,fr))
        outfile.write("  %8.4f to %8.4f\t%8.1f\t%6.4g\t%6.4g\t%6.4g\t%6.4g\t %6.4g \n" \
                      % (L[i], L[i + 1], C[i], AverageAmp[i], MaxAmp[i], AverageMean[i], MinValley[i], MaxPeak[i]))

    sum_val = float_sum(sum_damage)
    yf = ymax
    outfile.write("\n\n  Total Cycles = %g  hold=%d  NP=%d ymax=%g\n" % (summ, hold, num, yf))
    outfile.close()
    return sum_val
