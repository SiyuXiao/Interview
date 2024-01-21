import hashlib
with open('possible_uuids.txt', 'r') as possible_uuids:
	possible_uuids = [a[:36] for a in list(possible_uuids)]#the length of each line is 37 whose last one is \n
with open('clients.csv', 'r') as clients:
	clients = list(clients)[1:]
	uuid_md5 = []
	for a in clients:
		uuid_md5.append(a.split(',')[-1][:32])
possible_uuids_md5 = {}
for a in possible_uuids:
	m = hashlib.md5()
	m.update(a.encode('UTF-8'))
	possible_uuids_md5[m.hexdigest()] = a
uuid = []
for a in uuid_md5:
	uuid.append(possible_uuids_md5[a])
new = ['name,email,date,uuid_md5,uuid']
for i in range(len(uuid)):
	new.append(clients[i].split(',')[0]+','+clients[i].split(',')[1]+','+clients[i].split(',')[2] + ',' + uuid_md5[i] + ',' + uuid[i])
with open('new_clients.csv', 'w') as new_clients:
	for a in new:
		new_clients.write(a+'\n')