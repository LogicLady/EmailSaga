#!/usr/bin/python3.6

import cgi, os, pandas, sys
import cgitb; cgitb.enable()
from shutil import copyfileobj
from intercom.client import Client


form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
	file = "../files/" + fileitem.filename
	open(file, 'wb').write(fileitem.file.read())

	# intercom API extended access token
	intercom = Client(personal_access_token='dG9rOjQ2MmM2MzlkXzQwNzRfNGVkYl84YjYwXzkwZDVmNzcyMzcyMjoxOjA=')

	# create dataframe from input CSV which should be in the same directory
	df = pandas.read_csv(file, header=None, usecols=[0], names=['Email Address'])

	sites = [
		['Twitter', 'Twitter Username', [], 'Twitter URL', []],
		['Facebook', 'Facebook Username', [], 'Facebook URL', []],
		['LinkedIn', 'LinkedIn Username', [], 'LinkedIn URL', []],
		['Klout', 'Klout Username', [], 'Klout URL', []],
		['Vimeo', 'Vimeo Username', [], 'Vimeo URL', []],
		['GooglePlus', 'Google Plus Username', [], 'Google Plus URL', []],
		['Flickr', 'Flickr Username', [], 'Flickr URL', []],
		['Github', 'GitHub Username', [], 'GitHub URL', []],
		['Foursquare', 'FourSquare Username', [], 'FourSquare URL', []],
		['YouTube', 'YouTube Username', [], 'YouTube URL', []],
		['Myspace', 'MySpace Username', [], 'MySpace URL', []],
		['Tumblr', 'Tumblr Username', [], 'Tumblr URL', []]
	]
	others = ['Other Username', [], 'Other URL', [], 'Other Type', []]
	avatars = ['Avatar URL', []]
	titles = ['Job Title', []]

	site_list = []
	emailnum = 0

	for site in sites:
		site_list.append(site[0])

	for email in df['Email Address']:
		emailnum += 1
		intercom.users.create(email=email)
		user = intercom.users.find(email=email)
		avatars[1].append(user.avatar.image_url)
		if len(user.custom_attributes) > 0:
			if str(user.custom_attributes)[2:11] == 'job_title':
				titles[1].append(str(user.custom_attributes)[15:len(str(user.custom_attributes))-2])
			else: 
				print("Unknown Custom Attribute: " + user.custom_attributes)
		for profile in user.social_profiles:
			for site in sites:
				if profile.name == site[0]: 
					site[2].append(profile.username)
					site[4].append(profile.url)
			if profile.name not in site_list:
				others[1].append(profile.username)
				others[3].append(profile.url)
				others[5].append(profile.name)
		for l in (others[1], others[3], others[5], titles[1]):
			if len(l) < emailnum:
				l.append("")
		for site in sites:
			if len(site[2]) < emailnum: 
				site[2].append("")
			if len(site[4]) < emailnum: 
				site[4].append("")

	# add arrays to dataframe
	for site in sites:
		df[site[1]] = site[2]
		df[site[3]] = site[4]
	df[others[0]] = others[1]
	df[others[2]] = others[3]
	df[others[4]] = others[5]
	df[avatars[0]] = avatars[1]
	df[titles[0]] = titles[1]

	# Write dataframe back to input CSV
	df.to_csv(file, index=False)
	print('Content-Type:application/octet-stream; name="' + fileitem.filename + '";')
	print('Content-Disposition: attachment; filename="' + fileitem.filename + '"\n')
	sys.stdout.flush()
	with open(file,'rb') as f:
    		copyfileobj(f, sys.stdout.buffer)

else:
   print("Content-Type: text/html\n\n<html><body><p>No file was uploaded.</p></body></html>")