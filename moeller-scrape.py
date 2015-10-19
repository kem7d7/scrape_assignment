import urllib2, csv
import mechanize
from bs4 import BeautifulSoup

output = open('output.csv', 'w')
writer = csv.writer(output)

br = mechanize.Browser()
br.open('http://enrarchives.sos.mo.gov/enrnet/')

# Fill out the form
br.select_form(nr=0)
br["ctl00$MainContent$cboRaces"] = ["460006719"]

## actually click the button rather than submitting
req = br.click(name="ctl00$MainContent$btnCountyChange")
br.open(req)
html = br.response().read()

# Transform the HTML into a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

# Find the main table using both the "align" and "class" attributes
main_table = soup.find('table',
    {'class': 'electtable', 'id': 'MainContent_dgrdCountyRaceResults'}
    )

csv_body = []
rows = main_table.find_all('tr')
for row in rows:
    csv_row = []
    for col in row.find_all(['td','th']):
        if len(col.string.strip()) > 0:
            csv_row.append(col.string.strip())
    
    if (len(csv_row) > 0):
        csv_body.append(csv_row)

for row in csv_body:
    writer.writerow(row)







