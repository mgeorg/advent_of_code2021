
fill_pattern = '.'
for i in range(50):
  image = AddBorder(image, fill_pattern)
  fill_pattern = table[GetValue(fill_pattern*9)]
  image = DoLookup(image)

