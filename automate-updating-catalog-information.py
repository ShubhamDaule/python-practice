## Automate updating catalog information, Total 6 py scripts

##changeImage.py

#!/usr/bin/env python3
from PIL import Image
import os

path = "./supplier-data/images/"
for f in os.listdir("./supplier-data/images"):
    if f.endswith(".tiff"):
        split_f = f.split(".")
        name = split_f[0] + ".jpeg"
        im = Image.open(path + f).convert("RGB")
        im.resize((600, 400)).save("./supplier-data/images/" + name, "JPEG")



supplier_image_upload.py


#!/usr/bin/env python3
import requests
import os
# This example shows how a file can be uploaded using
# The Python Requests module

url = "http://localhost/upload/"
for f in os.listdir("./supplier-data/images"):
    if f.endswith(".jpeg"):
        with open('./supplier-data/images/' + f, 'rb') as opened:
            r = requests.post(url, files={'file': opened})


##run.py



#! /usr/bin/env python3
import os
import requests

fruits = {}
keys = ["name", "weight", "description", "image_name"]
index = 0
path = "./supplier-data/descriptions/"
img_path = "./supplier-data/images/"
for file in os.listdir("./supplier-data/descriptions"):
    with open(path + file) as f:
        for ln in f:
            line = ln.strip()
            if "lbs" in line:
                nline = line.split()
                wght = int(nline[0])
                fruits["weight"] = wght
                index += 1
            else:
                try:
                    fruits[keys[index]] = line
                    index += 1
                except:
                    fruits[keys[2]] = line
        index = 0
        split_f = file.split(".")
        name = split_f[0] + ".jpeg"
        for fle in os.listdir("./supplier-data/images"):
            if fle == name:
                fruits["image_name"] = name
        response = requests.post("http://<External_IP>/fruits/", json=fruits)
        fruits.clear()




##reports.py


#!/usr/bin/env python3
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_report(attachment, title, pharagraph):
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(attachment)
    report_title = Paragraph(title, styles["h1"])
    report_info = Paragraph(pharagraph, styles["BodyText"])
    table_style = [('GRID', (0, 0), (-1, -1), 1, colors.black),
                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                   ('ALIGN', (0, 0), (-1, -1), 'CENTER')]
    empty_line = Spacer(1, 20)

    report.build([report_title, empty_line, report_info])



##report_email.py

#!/usr/bin/env python3
import os
import datetime
import reports
import emails

dt = datetime.date.today().strftime("%B  %d, %Y")
date = "Processed Update on " + dt
names = []
weights = []
path = "./supplier-data/descriptions/"
for file in os.listdir("./supplier-data/descriptions"):
    with open(path + file) as f:
        for ln in f:
            line = ln.strip()
            if len(line) <= 10 and len(line) > 0 and "lb"not in line:
                fruit_name = "name: " + line
                names.append(fruit_name)
            if "lbs" in line:
                fruit_weight = "weight: " + line
                weights.append(fruit_weight)

summary = ""
for name, weight in zip(names, weights):
    summary += name + '<br />' + weight + '<br />' + '<br />'

if __name__ == "__main__":
    reports.generate_report("/tmp/processed.pdf", date, summary)
    sender = "automation@example.com"
    receiver = "<USERNAME>@example.com".format(os.environ.get('USER'))
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."

    message = emails.generate_email(sender, receiver, subject, body, "/tmp/processed.pdf")
    emails.send_email(message)





##emails.py



#!/usr/bin/env python3
import email.message
import mimetypes
import os.path
import smtplib


def generate_email(sender, recipient, subject, body, attachment_path):
    """Creates an email with an attachement."""
    # Basic Email formatting
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    # Process the attachment and add it to the email
    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)

    with open(attachment_path, 'rb') as ap:
        message.add_attachment(ap.read(),
                               maintype=mime_type,
                               subtype=mime_subtype,
                               filename=attachment_filename)

    return message


def generate_error_email(sender, recipient, subject, body):
    """Creates an email without an attachement."""
    # Basic Email formatting
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    return message


def send_email(message):
    """Sends the message to the configured SMTP server."""
    mail_server = smtplib.SMTP('localhost')
    mail_server.send_message(message)
    mail_server.quit()




## health_check.py


#!/usr/bin/env python3
import shutil
import psutil
import socket
import emails
import os

sender = "automation@example.com"
receiver = "<USERNAME>@example.com".format(os.environ.get('USER'))
body = "Please check your system and resolve the issue as soon as possible."

# Checks disk usage and sends email if available space < 20%
du = shutil.disk_usage("/")
du_prsnt = du.free/du.total * 100
if du_prsnt < 20:
    subject = "Error - Available disk space is less than 20%"
    message = emails.generate_error_email(sender, receiver, subject, body)
    emails.send_email(message)

# Checks CPU usage and sends email if usage >80%
cpu_prsnt = psutil.cpu_percent(1)
if cpu_prsnt > 80:
    subject = "Error - CPU usage is over 80%"
    message = emails.generate_error_email(sender, receiver, subject, body)
    emails.send_email(message)

# Checks for available memory, if < 500mb sends an email
mem = psutil.virtual_memory()
trs = 500 * 1024 * 1024  # 500MB
if mem.available < trs:
    subject = "Error - Available memory is less than 500MB"
    message = emails.generate_error_email(sender, receiver, subject, body)
    emails.send_email(message)

# Checks hostname and if cannot be resolved to "127.0.0.1" sends an email
hostname = socket.gethostbyname('localhost')
if hostname != '127.0.0.1':
    subject = "Error - localhost cannot be resolved to 127.0.0.1"
    message = emails.generate_error_email(sender, receiver, subject, body)
    emails.send_email(message)
