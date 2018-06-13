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
ccs = config['cc']
bccs = config['bcc']

# CC
cc_string = ''
if len(ccs) > 0:
  cc_string = '-cc'
  for cc in ccs:
    cc_string += ' "' + cc + '"'

# BCC
bcc_string = ''
if len(bccs) > 0:
  bcc_string += '-bcc'
  for bcc in bccs:
    bcc_string += ' "' + bcc + '"'

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
    to = row['to'].strip()
    print('Sending email to', to)
    email_filename = default_email_filename
    try:
        email_filename = row['filename'].strip()
    except:
        pass
    email_file = open(email_filename)
    subject = process_template(email_file.readline().strip(), row)
    body = ''
    while True:
        line = email_file.readline()
        if not line:
            break
        if body == '' and line.strip() == '':
        	continue
        body += process_template(line, row)
    email_file.close()
    mapping = {
        'tls': tls,
        'from': from_addr,
        'to': to,
        'cc_string': cc_string,
        'bcc_string': bcc_string,
        'server': server,
        'port': port,
        'username': username,
        'password': password,
        'subject': subject,
        'body': body
    }
    os.system('sendemail -o tls=%(tls)s -f "%(from)s" -t "%(to)s" %(cc_string)s %(bcc_string)s -s %(server)s:%(port)s -xu "%(username)s" -xp "%(password)s" -u "%(subject)s" -m "%(body)s"' % mapping)
