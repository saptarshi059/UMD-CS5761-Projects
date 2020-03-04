#who are you?
#what are monkeys?
#who was george washington?

'''
		s = wikipedia.summary(match_operation.group(3))

		s = re.sub(r'\(listen\);','',s)
		s = re.sub(r'\([^)]*\)', '', s)
		s = re.sub(r'  ',' ',s)
		s = re.sub(r'\s\.','.',s)
		#s = s.lower()

		rewriten_query = match_operation.group(3) + ' ' + match_operation.group(2)

		res = re.findall(re.escape(rewriten_query) + r'[^.]*\.' ,s)

		string = ' '.join(x for x in res)
		'''
		string = 'asd'
