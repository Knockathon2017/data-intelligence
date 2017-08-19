import json

look = {}
meta = open('build/meta.csv').read().strip().split("\n")
for line in meta[1:]:
	c = line.split(",")
	if c[1] == '':
		c[1] = 10000
	look[c[0].split('US')[1]] = int(float(int(c[1])))/10

data = open('build/mappop.json').read()
data = json.loads(data)

for k,v in data.iteritems():
	if k == 'objects':
		for each in v['counties']['geometries']:
			each['properties']['population'] = look[each['id']]

print json.dumps(data)			