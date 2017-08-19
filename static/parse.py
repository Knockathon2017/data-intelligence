da = open('data_crime.csv').read().strip().split("\n")


def clean(get):
	get = get.replace("'","").replace(".","").strip()
	get = get.replace('"','').replace('-','').replace(' of ','').replace(' ','')
	return get


hci_states = 'Arkansas,California,Maryland,North Carolina,New Jersey,Ohio,Pennsylvania,South Carolina,Texas'
hci = 'AK,CA,MD,NC,NJ,OH,PA,SC,FL'
# hci = 'TX'

print clean('US') + " ;"
visited = {}
for i, line in enumerate(da):
	num = line.split("	")[1]
	a = line.split("	")[0]

	c = a.split(", ")
	if len(c) > 1:

		if c[1] not in hci:
			continue

		if c[1] not in visited:
			visited[c[1]] = 1
			print clean(c[1]) + " ;"
			print clean('US') + " -> " + clean(c[1]) + " ;"
		
		if c[0] not in visited:
			up = c[0]
			visited[c[0]] = 1
		else:
			up = c[0]
			visited[up] = 1
		
		print clean(up) + " ;"
		print clean(c[1]) + " -> " + clean(up) + " ;"