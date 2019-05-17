# import json
# # def process():
# training_data = []
# with open('data.json') as json_file:
#     training_data = json.load(json_file)['data']
# classes = []
# for x in training_data:
# 	if x['class'] not in classes:
# 		print(x['class'])
# 	classes.append(x['class'])
# exit(0)
def process(action, text):
	if action == 'greeting':
		text = "I am fine, Hope you are well too!"
		return returnData(action, text, None)

	if action == 'setting_alarm':
		date = extractDate(text)
		text = 'Okay, your alarm is set for ' + str(date.strftime("%A %B %d, at %H:%M"))
		data = {'date': str(date)}
		return returnData(action, text, data)

	if action == 'goodbye':
		text = "Goodbye, Hope to see you again!"
		return returnData(action, text, None)

	if action == 'contacts':
		name = NER(text, 'PERSON')
		if name:
			text = "Checking " + name + "'s contacts"
		else:
			text = "Checking your contacts list"
		data = {name: name}
		return returnData(action, text, data)

	if action == 'meeting':
		date = extractDate(text)
		text = 'Scheduling a meeting at ' + str(date.strftime("%A %B %d, at %H:%M"))
		data = {'date': str(date)}
		return returnData(action, text, data)

	if action == 'text_message':
		name = NER(text, 'PERSON')
		text = "Sending a text message"
		if(name):
			text = text + " to " + name
		data = {name: name}
		return returnData(action, text, data)

	if action == 'asking_for_events':
		text = "Checking your calender"
		return returnData(action, text, None)

	if action == 'send_email':
		name = NER(text, 'PERSON')
		text = "Sending an Email"
		if(name):
			text = text + " to " + name
		data = {name: name}
		return returnData(action, text, data)

	if action == 'locatefriends':
		name = NER(text, 'PERSON')
		if not name:
			name = 'friend'
		text = "Checking " + name + "'s Location on Maps"
		data = {name: name}
		return returnData(action, text, data)

	if action == 'Maps_direction':
		text = "Opening maps"
		return returnData(action, text, None)

	if action == 'LocalBusinesses':
		name = NER(text, 'ORGANIZATION')
		text = "Opening maps"
		if name:
			text = text + ', finding ' + name
		data = {name: name}
		return returnData(action, text, data)

	if action == 'MUSIC':
		import re
		text = text.lower()
		songName = re.sub(r' on (anghami|soundcloud|spotify|youtube)', '', re.sub(r'^(play|stream|shuffle).*?\s', '', text));
		platform = re.findall(r"(anghami|soundcloud|spotify|youtube)", text)
		if(platform.__len__() > 0):
			platform = str(platform[0])
		else:
			platform = 'music'
		text = 'Okay, asking ' + platform + ' to play ' + songName + '...'
		data = {
			'songName': songName,
			'platform': platform
		}
		return returnData(action, text, data)

	if action == 'NOTES':
		text = "Noted!"
		return returnData(action, text, None)

	if action == 'PHONECALL':
		name = NER(text, 'PERSON')
		text = "Calling " + name
		data = {name: name}
		return returnData(action, text, data)

	if action == 'REMINDER':
		date = extractDate(text)
		text = 'Setting a reminder at ' + str(date.strftime("%A %B %d, at %H:%M"))
		data = {'date': str(date)}
		return returnData(action, text, data)

	if action == 'SEARCHWEB':
		import re
		query = re.sub(r'(search|search for|search the web|google|do a web search)', '', text.lower());
		text = "Doing a web search " + query
		data = {query: query}
		return returnData(action, text, data)

	if action == 'WEATHER':
		location = NER(text, 'LOCATION')
		text = "Checking the weather state"
		if location:
			text = text + ' in ' + location
		else:
			location = 'Cairo'
			text = text + ' in ' + location
		data = {location: location}
		return returnData(action, text, data)

def NER(text, tagName):
	import nltk
	from nltk.tag import StanfordNERTagger
	from nltk.tokenize import word_tokenize
	st = StanfordNERTagger('./english.all.3class.distsim.crf.ser.gz', './stanford-ner.jar', encoding='utf-8')
	for sent in nltk.sent_tokenize(text):
	    tokens = nltk.tokenize.word_tokenize(sent)
	    tags = st.tag(tokens)
	    name = []
	    for tag in tags:
	        if tag[1]==tagName: name.append(tag[0])
	    name = " ".join(name)
	return name

def extractDate(text):
	import parsedatetime
	from datetime import datetime
	cal = parsedatetime.Calendar()
	time_struct, parse_status = cal.parse(text)
	date = datetime(*time_struct[:6])
	return date

def returnData(action, text, data):
	return {
		'action': action,
		'text': text,
		'data': data
	}
