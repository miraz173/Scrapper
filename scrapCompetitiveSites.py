import re
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from operator import itemgetter
from selenium.webdriver.edge.service import Service as EdgeService

month = {"january": "01", "jan": "01", "february": "02", "feb": "02", "march": "03", "mar": "03", "april": "04",
         "apr": "04", "may": "05", "june": "06", "jun": "06", "july": "07", "jul": "07", "august": "08", "aug": "08",
         "september": "09", "sep": "09", "october": "10", "oct": "10", "november": "11", "nov": "11", "december": "12",
         "dec": "12", "January": "01", "Jan": "01", "February": "02", "Feb": "02", "March": "03", "Mar": "03",
         "April": "04", "Apr": "04", "May": "05", "June": "06", "Jun": "06", "July": "07", "Jul": "07", "August": "08",
         "Aug": "08", "September": "09", "Sep": "09", "October": "10", "Oct": "10", "November": "11", "Nov": "11",
         "December": "12", "Dec": "12"}
reMonth = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
           '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
weekday_to_num = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 " \
             "Safari/537.36"

service = EdgeService(executable_path='path/to/edge/driver.exe')
options = webdriver.EdgeOptions()
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Edge(service=service, options=options)


temp = []
ccRngContest = []
ccNxtContest = []
driver.get('https://www.codechef.com/contests/')
time.sleep(2)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()
contests = soup.find_all('tr')
for tr in contests:
    if "Participants" in tr.text:
        break
    child_elements = tr.find_all('td')
    for element in child_elements:
        if element.text == " ":
            continue
        element = element.text.replace("Code", "")
        element = element.replace("Name", "")
        element = element.replace("Starts in", "")
        element = re.sub(r"\bDuration(\d+)\b", r"\1", element)
        element = re.sub(r"\bStart(\d+)\b", r"\1", element)
        temp.append(element)
        # print(element.text, end="  ")
    # print()
    if len(temp) == 0:
        continue
    if "Ongoing" in tr.parent.parent.parent.parent.parent.parent.text:
        links = tr.find('a')
        if links is not None:
            temp.append(links.get('href'))
        ccRngContest.append(temp)
        temp = []
        # print(ccRngContest, end="  ")
        continue
    x = re.sub(r'\d+\s+(\w+)\s+\d+(\w+)\s+\d+.\d+', r'\1', temp[2])
    numbers = re.findall(r'\d+\.\d+|\d+', temp[2])
    numbers.insert(1, month[x])
    temp[2] = numbers
    temp = temp[1:]
    temp[3] = re.findall(r'\d+\.\d+|\d+', temp[3])
    links = tr.find('a')
    if links is not None:
        temp.append(links.get('href'))
    x = temp[1][0]    # swap year and day number
    temp[1][0] = temp[1][2]
    temp[1][2] = x
    ccNxtContest.append(temp)
    temp = []
# print(ccRngContest)
# print(ccNxtContest)

options.add_argument('--headless')
driver = webdriver.Edge(service=service, options=options)

temp = []
contests = []
cfRngContest = []
cfNxtContest = []
driver.get('https://www.codeforces.com/contests/')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')
trs = soup.find_all('tr')  # get all table rows
trs = trs[1:7]  # keep 6 table rows, 1-6
for tr in trs:
    if "Name" in tr.text:
        continue
    count = 0
    for col in tr:
        count += 1
        z = col.text
        z = z.replace("\n\n", "")
        z = z.replace("\n", " ")
        z = z.replace("  ", "")
        if z == "\n" or z == "" or z == " ":
            continue
        temp.append(z)
        if count == 2:
            continue
    temp[0] = temp[0].replace("\n", "")
    temp[0] = temp[0][1:]
    if len(temp) == 6:
        del temp[1]
    x = re.search(r"[A-Z][a-z]+", temp[1])
    if x:
        try:
            x = month[x.group(0)]
            temp[1] = re.findall(r"\d+", temp[1])
            temp[1].insert(1, x)
            temp[1] = temp[1][:-1]  # strip last element as it actually gmt+6
        except KeyError as e:
            print(e)

    x = temp[1][0]    # swap year and day number
    temp[1][0] = temp[1][2]
    temp[1][2] = x
    cfNxtContest.append(temp)
    temp = []
# print(cfNxtContest)

url = 'https://atcoder.jp/contests/'
driver.get(url)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(1)
temp = []
contests = []
acRngContest = []
acNxtContest = []
soup = BeautifulSoup(driver.page_source, 'lxml')
trs = soup.find("div", id="contest-table-upcoming")
trs = trs.find_all('tr')
trs = trs[1:]
for tr in trs:
    for col in tr:
        col = col.text.replace("\n", "")
        if col == '':
            continue
        temp.append(col)
    temp[0] = re.findall(r"\d+", temp[0])
    k = datetime.datetime(int(temp[0][0]), int(temp[0][1]), int(temp[0][2]), int(temp[0][3]), int(temp[0][4]))
    k = k - datetime.datetime.now()
    # x = temp[0][0]
    # temp[0][0] = temp[0][2]
    # temp[0][2] = x
    x = temp[0]
    temp[0] = temp[1]
    temp[1] = x
    temp[3] = k
    acNxtContest.append(temp)
    temp = []
print(acNxtContest)

url = 'https://leetcode.com/contest/'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()
trs = soup.find_all("div", class_="h-[54px]")
temp = []
contests = []
lcRngContest = []
lcNxtContest = []
for tr in trs:
    if "Ended" in tr.text:
        continue
    for col in tr:
        col = col.text.replace("\n", "")
        temp.append(col)
    x = re.findall(r"\b[A-Z][a-z]+\b", temp[1])
    x = weekday_to_num[x[0]]
    today = datetime.date.today()
    x = today + datetime.timedelta((x-1 - today.weekday()) % 7)
    x = re.findall(r"\d+", str(x))
    y = re.findall(r"\d+", temp[1])
    if "PM" in temp[1]:
        y[0] = int(y[0])+12
    y = datetime.time(int(y[0]), int(y[1]))
    x = datetime.datetime.combine(x, y)
    print(x)
    temp[1] = [str(x.year), str(x.month), str(x.day), str(x.hour), str(x.minute)]
    temp.append(x)
    x = x-datetime.datetime.now()
    print(str(x))
    temp.append(x)
    print(temp)
    contests.append(temp)
    temp = []
lcNxtContest = contests
print(lcNxtContest)

if driver:
    driver.quit()

from operator import itemgetter

allContests = ccNxtContest+cfNxtContest+acNxtContest+lcNxtContest
sorted_list = sorted(allContests, key=itemgetter(1))
for i in sorted_list:
    print(i)

def html_write_contests(sorted_list, output_filename):
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>Upcoming Contests</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            .sub-table td {
                border: none;
            }
        </style>
    </head>
    <body>
    <table>
        <thead>
            <tr>
                <th>Time Left</th>
                <th>Contest Title</th>
                <th>Contest Time</th>
                <th>Duration</th>
                <th>Link</th>
            </tr>
        </thead>
        <tbody>"""

    for i in sorted_list:
        time_left=datetime.datetime(int(i[1][0]), int(i[1][1]), int(i[1][2]), int(i[1][3]), int(i[1][4]))-datetime.datetime.now()
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_left_str = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"

        time_when=f"{i[1][3]}:{i[1][4]}</br>{i[1][2]}/{i[1][1]}/{i[1][0]}"

        html += f"<tr><td>{time_left_str}</td><td>{i[0]}</td><td>{time_when}</td><td>{i[2] if i[2]!=i[-1] else ''}</td><td><a href={i[-1]}>{i[-1]}</a></td></tr>"

    html += "\n</tbody></table></body></html>"

    # Save the output
    with open(output_filename, "w") as f:
        f.write(html)

output_html_filename="upcoming_contests.html"
html_write_contests(sorted_list, output_html_filename)

# Open created output file
import webbrowser
webbrowser.open(output_html_filename)