"""
Convert to actual test for testing candle creation works properly
"""

references = [1, 3, 5, 15, 30, 60, 120, 240, 360, 720, 1440, 4320, 10080]

minutes = 15

for i, j in enumerate(references):
  if j == minutes:
    for k in range(i-1, -1, -1):
      l = minutes / references[k]
      if l.is_integer():
        index = k
        break

print(f"{int(minutes/references[index])} {references[index]} minute candles.")

test = ["a", "b", "c", "d"]
for i in range(20):
  if test[i]:
    print(test[i])