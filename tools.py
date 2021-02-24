def parseList(path):
	with open(path, 'r', encoding='utf8') as file:
		ls = file.readlines()
		dic = {}
		for line in ls:
			values = line.strip().split(',')
			dic[values[2]] = (values[0], values[1], values[3])
	return dic

def abb2name(s, ABBS):
	if s is None:
		return None
	try:
		return ABBS[s][0]
	except KeyError:
		return None

def abb2clan(s, ABBS):
	if s is None:
		return None
	try:
		return ABBS[s][1]
	except KeyError:
		return None

def abb2event(s, ABBS):
	if s is None:
		return None
	try:
		return ABBS[s][2]
	except KeyError:
		return None

def acabb(s, ABBS):
	s = s.strip().upper()
	if len(s) >= 3:
		if s[:3] in ABBS.keys():
			return s[:3]
		s = s[:2]	
	for abb in ABBS.keys():
		if s == abb[:2]:
			return abb
	return None

def loadMR(team, MASTERROSTER, service):
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=MASTERROSTER, range=f'{team}!C12:E56').execute()
	return result.get('values', [])

def loadRoster(w, DASHBOARD, service):
	week = 'Week ' + w[1:]

	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=DASHBOARD, range=f"{week}!D17:F36").execute()
	return result.get('values', [])

def isInt(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

def s2h(n):
	n = int(n)
	if n==0:
		return "0s"
	ls = [int(n/3600), int(n/60)%60, n%60]
	cad = ""
	if ls[0] != 0:
		cad+=f"{ls[0]}h "
	if ls[1] != 0:
		cad+=f"{ls[1]}m "
	if ls[2] != 0:
		cad+=f"{ls[2]}s"
	return cad

def urng(n, m):
	res = [-1] * n
	count = 0
	a = 0

	while count < n:
		a = random.randint(0, m-1)
		if a not in res:
			res[count] = a
			count += 1

	return res