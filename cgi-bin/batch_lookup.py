#!/usr/bin/python3.6

import cgi, os, pandas, sys
import cgitb; cgitb.enable()
from shutil import copyfileobj
from intercom.client import Client

# Grab data from form at emailsa.ga/batch.html
form = cgi.FieldStorage()

# Get filename here
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
	# open the uploaded file from files directory
	file = "../files/" + fileitem.filename
	open(file, 'wb').write(fileitem.file.read())

	# intercom API extended access token
	intercom = Client(personal_access_token='#########################')

	# create dataframe from uploaded CSV - it should have emails in first column and no header is needed
	df = pandas.read_csv(file, header=None, usecols=[0], names=['Email Address'])
	
	# Create arrays for lookup/output data in order to separate by social media platform
		# 1st object is the lookup value for API call results, to separate by website
		# 2nd object is CSV column name for the username result, the 3rd is the actual result from API call
		# 3rd object is CSV column name for the URL result, the 4th is the actual result from API call
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
		['Tumblr', 'Tumblr Username', [], 'Tumblr URL', []],
		['Wordpress', 'Wordpress Username', [], 'Wordpress URL', []]
	]
	# Creates arrays for lookup/output data for miscellaneous information
		# Includes profiles not defined in the sites array, avatar URL, and job title
	others = ['Other Username', [], 'Other URL', [], 'Other Type', []]
	avatars = ['Avatar URL', []]
	titles = ['Job Title', []]
	
	# creates list of only the lookup values from sites array
	site_list = []
	for site in sites:
		site_list.append(site[0])

	# initiates variable for counting the result number
	emailnum = 0
	
	# main code to run for each email address
	for email in df['Email Address']:
		# keep count of result number
		emailnum += 1
		
		# call intercom API
		intercom.users.create(email=email)
		user = intercom.users.find(email=email)
		
		# add avatar URL to array
		avatars[1].append(user.avatar.image_url)
		
		# if custom attributes are present and include job title, append result to job title array
		if len(user.custom_attributes) > 0:
			if str(user.custom_attributes)[2:11] == 'job_title':
				titles[1].append(str(user.custom_attributes)[15:len(str(user.custom_attributes))-2])
			else: 
				print("Unknown Custom Attribute: " + user.custom_attributes)
				
		# code to run for each social media profile result		
		for profile in user.social_profiles:
			# add the result to the appropriate array in sites, based on platform
			for site in sites:
				if profile.name == site[0]: 
					site[2].append(profile.username)
					site[4].append(profile.url)
			# add the result to 'others' array if it is not defined in sites array		
			if profile.name not in site_list:
				others[1].append(profile.username)
				others[3].append(profile.url)
				others[5].append(profile.name)
		
		# add a blank result to the different arrays if no result was found (so that the rows match up properly)		
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
	
	# Initiate file download for updated CSV
	print('Content-Type:application/octet-stream; name="' + fileitem.filename + '";')
	print('Content-Disposition: attachment; filename="' + fileitem.filename + '"\n')
	sys.stdout.flush()
	with open(file,'rb') as f:
    		copyfileobj(f, sys.stdout.buffer)

# Print error message if no file was uploaded.
else:
   print("Content-Type: text/html\n\n<html><body><p>No file was uploaded.</p></body></html>")
