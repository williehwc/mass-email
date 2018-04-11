import json, csv, getpass, os, re

default_email_filename = 'email.txt'

# Read config file
config = json.load(open('config.json'))
server = config['server']
port = config['port']
tls = config['tls'] # Choices: yes, no, auto
from_addr = config['from']
username = config['username']
password = getpass.getpass('Enter your SMTP password:')

# Process template function
def process_template(string, replacements):
    variables_to_replace = re.findall('(?<=\{)\S+(?=\})', string)
    for variable in variables_to_replace:
        string = string.replace('{' + variable + '}', replacements[variable])
    return string

# Read email list and send emails
reader = csv.reader(open('list.csv'))
header = next(reader)
rows = [dict(zip(header, row)) for row in reader]
for row in rows:
    to = row['to']
    email_filename = default_email_filename
    try:
        email_filename = row['filename']
    except:
        pass
    email_file = open(email_filename)
    subject = process_template(email_file.readline(), row)
    body = ''
    while True:
        line = email_file.readline()
        if not line:
            break
        body += process_template(line, row)
    email_file.close()
    mapping = {
        'tls': tls,
        'from': from_addr,
        'to': to,
        'server': server,
        'port': port,
        'username': username,
        'password': password,
        'subject': subject,
        'body': body
    }
    os.system('sendemail -o tls=%(tls)s -f "%(from)s" -t "%(to)s" -s %(server)s:%(port)s -xu "%(username)s" -xp "%(password)s" -u "%(subject)s" -m "%(body)s"' % mapping)
