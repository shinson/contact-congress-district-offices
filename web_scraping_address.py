from bs4 import BeautifulSoup
import urllib2

# Create the list of districts using a csv file listing all the districts
with open("all_districts.csv", "r") as district_list_file:
	district_list = district_list_file.read().replace("_", "").split("\r\n")
	district_list.pop(0)

district_list_file.close()

#Make a list of state abbreviations for senators so that we can access the webpage for each Senator
new_state_abbrevs=[]
state_abbrevs = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
for state in state_abbrevs:
	new_state_abbrevs.append(state+'SR')
	new_state_abbrevs.append(state+'JR')

#We'll start with the Representatives. In the file is a list of all the districs in the country. Using a for loop the web address gets maniplated to include each district.
#The for loop uses beatiful soup to access the address
#There is a second for loop since each representative has a different number of district offices. In order to ensure we get all the offices, we used this second for loop.
#Then we write the info into a CSV file, but since the Address does not have a comma between the State and Zip5, we have to add it in
# We repeat the same thing for the senators, but instead we use the new_state_abbrevs list
with open("all_districts_info.txt", "w") as district_file_updated:
	district_file_updated.write("District, Street_Address, City, State, ZipCode\n")
	for districts in district_list:
		html = urllib2.urlopen('http://www.contactingthecongress.org/cgi-bin/newmemberbio.cgi?member='+ districts).read()
		soup = BeautifulSoup(html)
		addr_list = soup.find_all('input', {'name':'q'})
		for index, addr in enumerate(addr_list):
			district_file_updated.write(districts+",");
			old=addr_list[index].get('value')
			position=addr_list[index].get('value').find(districts[:2]) 
			new = old[:position+2]+','+old[position+2:]
			district_file_updated.write(new);
			district_file_updated.write('\n')
	for senator in new_state_abbrevs:
		html = urllib2.urlopen('http://www.contactingthecongress.org/cgi-bin/newmemberbio.cgi?member='+ senator).read()
		soup = BeautifulSoup(html)
		addr_list = soup.find_all('input', {'name':'q'})
		for index, addr in enumerate(addr_list):
			district_file_updated.write(senator+",");
			old=addr_list[index].get('value')
			position=addr_list[index].get('value').find(senator[:2]) 
			new = old[:position+2]+','+old[position+2:]
			district_file_updated.write(new);
			district_file_updated.write('\n')

district_file_updated.close()

