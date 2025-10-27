raw_a = [1, 2, 3, 4]
new_b = [1, 2, 4, 5]
c = raw_a

raw_c = [x for x in raw_a if x != new_b]
print(raw_c)