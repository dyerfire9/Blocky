colours = {}
children = [(199, 44, 58), (1, 128, 181), (234, 62, 112), (75, 196, 213), (75, 196, 213)]
for child in children:
    if child not in colours:
        colours[child] = 1
    else:
        colours[child] += 1
#colours = {(2, 3, 4): 2, "no": 5, "say": 7}
sorted_d = sorted(colours.items(), key=lambda x: x[1], reverse = True)
print(sorted_d)
print(sorted_d[0])
print(sorted_d[0][0])
