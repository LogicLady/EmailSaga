#!/usr/bin/python3.6

import cgi, os, pandas, sys
import cgitb; cgitb.enable()
from intercom.client import Client

form = cgi.FieldStorage()
email_input = form.getvalue('email')

# intercom API extended access token
intercom = Client(personal_access_token='dG9rOjQ2MmM2MzlkXzQwNzRfNGVkYl84YjYwXzkwZDVmNzcyMzcyMjoxOjA=')
intercom.users.create(email=email_input)
search = intercom.users.find(email=email_input)
print("Content-Type: text/html\n\n")
print("<div class='result' style='font-family: Arial, Helvetica, sans-serif; text-align: center; margin: 0px 0px 50px 0px;'>")
  
if str(search.avatar.image_url) != 'None':
  print("<a href='" + str(search.avatar.image_url) + "' target='_blank'><img src='" + str(search.avatar.image_url) + "' alt='Avatar' style='width: 25%; border-radius: 5px; display: block; margin-left: auto; margin-right: auto;'></a>")

if len(search.custom_attributes) > 0:
  attr = str(search.custom_attributes)
  print("<br>Job Title: " + attr[15:len(attr)-2] + "<br><br>")
  
for profile in search.social_profiles:
  username = str(profile.username)
  name = str(profile.name)
  url = str(profile.url)
  print("<h2><a href='"+ url + "' target='_blank'>" + name + "</a></h2>")
  if username == 'None':
    print("<br>")
  else:
    print("Username: " + username + "<br><br>")

print("</div>")