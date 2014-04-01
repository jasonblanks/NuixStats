import sys
import sys, stat, os, re, time, datetime
from datetime import timedelta
from datetime import date
from time import mktime

MATTERS = []
SERVERS = [r'\\server\f$\Nuix_Cases', r'\\server\g$\Nuix_Cases']

class Matter():
	def __init__(self):
		self.case_name = None
		self.used = 0
		self.total_count = []
		self.total_size = []
		self.excluded_count = []
		self.excluded_size = []
		self.included_count = []
		self.included_size = []


print "server locations being searched:"
for server in SERVERS:
	print server+"\n"


print "Delta is the time frame to search within.  Delta is mesure in days. Please enter the number of days to use, note 0 means no delta used.\n"
d = 0
#d = sys.argv



for server in SERVERS:
	for root, dirs, files in os.walk(server):
		for file in files:
			if file.startswith('processingReport'):
				temp_matters = []
				for case in MATTERS:
					temp_matters.append(case.case_name)
				case_name = None
				temp = open(os.path.join(root,file),'r')
				ctime = time.ctime(os.path.getctime(os.path.join(root,file)))
				for line in temp:
					if line.startswith('case_name'):
						line = line.strip()
						line2 = line.split(' ')
						case_name = line2[1]
				temp.close()
				if case_name not in temp_matters:
					NewMATTER = Matter()
					NewMATTER.case_name = case_name
					temp = open(os.path.join(root,file),'r')
					for line in temp:
						line = line.strip()
						if line.startswith(r'total_count:'):
							line2 = line.split(r' ')
							total_count = line2[1]
							NewMATTER.total_count.append((total_count, ctime))
						elif line.startswith('total_size:'):
							line2 = line.split(' ')
							total_size = line2[1]
							NewMATTER.total_size.append((total_size, ctime))
						elif line.startswith('excluded_count:'):
							line2 = line.split(' ')
							excluded_count = line2[1]
							NewMATTER.excluded_count.append((excluded_count, ctime))
						elif line.startswith('excluded_size:'):
							line2 = line.split(' ')
							excluded_size = line2[1]
							NewMATTER.excluded_size.append((excluded_size, ctime))
						elif line.startswith('included_count:'):
							line2 = line.split(' ')
							included_count = line2[1]
							NewMATTER.included_count.append((included_count, ctime))
						elif line.startswith('included_size:'):
							line2 = line.split(' ')
							included_size = line2[1]
							NewMATTER.included_size.append((included_size, ctime))
					temp.close()
					MATTERS.append(NewMATTER)
					continue

				elif case_name in temp_matters:
					for case in MATTERS:
						if case.case_name == case_name:
							temp = open(os.path.join(root,file),'r')
							for line in temp:
								line = line.strip()
								if line.startswith("total_count:"):
									line2 = line.split(' ')
									total_count = line2[1]
									case.total_count.append((total_count, ctime))
								elif line.startswith('total_size:'):
									line2 = line.split(' ')
									total_size = line2[1]
									case.total_size.append((total_size, ctime))
								elif line.startswith('excluded_count:'):
									line2 = line.split(' ')
									excluded_count = line2[1]
									case.excluded_count.append((excluded_count, ctime))
								elif line.startswith('excluded_size:'):
									line2 = line.split(' ')
									excluded_size = line2[1]
									case.excluded_size.append((excluded_size, ctime))
								elif line.startswith('included_count:'):
									line2 = line.split(' ')
									included_count = line2[1]
									case.included_count.append((included_count, ctime))
								elif line.startswith('included_size:'):
									line2 = line.split(' ')
									included_size = line2[1]
									case.included_size.append((included_size, ctime))
							temp = open(os.path.join(root,file),'r')

for i in MATTERS:
	print "\n"+i.case_name
	#print i.total_size
	#print i.included_count
	#print i.included_size
	sum = 0
	if d == 0:
		for x in i.total_size:
			sum = int(sum)+int(x[0])
		#print "total_size ="+str(sum)
	else:
		for x in i.total_size:
			dif = (date.today() - timedelta(days=d))
			t  = datetime.datetime.strptime(x[1], "%a %b %d %H:%M:%S %Y")
			if t.date() >= dif:
				#print str(mktime(t))+" : "+str(mktime(timedelta(days=30)))
				sum = int(sum)+int(x[0])
	print "total_size ="+str(sum)
