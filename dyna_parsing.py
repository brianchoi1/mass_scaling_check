# fname = 'D:\\workothers\\timestep_check\\11'

# data = open(fname).readlines()      #fname = 'D:/LGE/1.1 work_others/damage_ratio/new_ver4/17'
# start = 0

# for i, line in enumerate(data):
#     if 'TimeStep' in line:
#         start = i

# dd = float(data[start][20:35].replace(" ", ""))
# print(dd)



# fname = 'D:\\workothers\\timestep_check\\2.k'

# data = open(fname).readlines()      #fname = 'D:/LGE/1.1 work_others/damage_ratio/new_ver4/17'
# start = 0

# for i, line in enumerate(data):
#     line = line.lower()
#     if '*control_timestep' in line:
#         start = i
#         break
# while '$' in data[start+1]:
#     start += 1
# start += 1
# tssfac = (data[start][10:20].replace(" ", ""))
# dt2ms = (data[start][40:50])

# # fw = open('2_1.k', 'w')
# # # for line in data:
# # #     fw.write(line.replace(old_str, new_str))
# # fw.close()

# print(start)
no = -1.5E-7
# print('[{0:8e}] [{1:>5e}] [{2:>5e}]'.format(11544435,-2544254,35454343))
dd = (format(no, '.3E'))
print('d')