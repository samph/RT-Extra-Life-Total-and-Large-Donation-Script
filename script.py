import requests, json
from time import sleep

total = 0;
previouslyOutputDonations = []
#TODO - grab list of participants from /teaminfo/21514 api call
participants = ["144746", "167386", "191395"]
apiServer = "http://192.168.1.167:8081"
outputDonationAbove = 100;

while(1):
	try:
		r = requests.get(apiServer + "/teamgoal/21514")
		if(r.status_code==200):
			parsed_json = json.loads(r.content)

			raised = parsed_json["raised"];
			if(raised > total):
				total = raised;
				print "Latest total is $" + str(total)

			sleep(1)
		else:
			print r.status_code


		for p in participants:
			r = requests.get(apiServer + "/recentDonations/"+p)
			if(r.status_code==200):
				parsed_json = json.loads(r.content)
				for x in range(0,len(parsed_json["recentDonations"])):
					name = parsed_json["recentDonations"][x]["name"]
					dollars = name.split('$')
					#Grab the value after the $ symbol
					if (len(dollars)>1):
						#Throw away everything after the decimal place.
						donation = dollars[1][:-4]
						#Throw away any commas (999+)
						if(int(donation.replace(",", ""))>outputDonationAbove):
							if(name not in previouslyOutputDonations):
								print name + " ("+p+")"
								previouslyOutputDonations.append(name)
			else:
				print r.status_code
	except requests.exceptions.ConnectionError:
		print "opps!"	

