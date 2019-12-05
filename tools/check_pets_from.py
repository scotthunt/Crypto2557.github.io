
import json


with open('app/static/json/pets.json') as f:
	pets = json.load(f)
f.close();


reverse = {}
max = 0

for key, item in pets.items():
	for i in item["from"]:
		if i in reverse:
			print('Error: duplicate at {}'.format(i))
			#exit(1)
		reverse[i] = key
		if i > max:
			max = i

sorted_reverse = sorted(reverse.items())

for i in range(1, max):
	if i % 5 not in (0, 1):
		continue
	if i not in reverse:
		print('Error: missing {}'.format(i))
		#exit(1)

for i in range(1, max):
	if i % 40 == 0:
		print("")
	if i % 5 != 1:
		continue
	print('{:3d}: {:25s} {:3d}: {:20s}'.format(i, reverse[i], i+4, reverse[i+4]))

