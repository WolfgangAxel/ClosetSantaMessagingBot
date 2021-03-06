#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CSMB.py
#  
#  2016 Keaton Brown <linux.keaton@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  

#################
#    Globals    #
#################

BOTMASTER = ""						# Your personal reddit account goes here

MYNAME = "Closet Stanta Postman"	# Can be different from the bot's account name
BOTFREQUENCY = 120					# Time in seconds between refreshes

# Also change botFlair below if you wish

#################
#    Modules    #
#################

try:
	mod='os'
	from os import path,mkdir
	mod='sys'
	from sys import path as moduleDir
	mod="time"
	from time import sleep,time
	mod='praw'
	import praw
	mod='OAuth2Util'
	import OAuth2Util
except:
	print "Module '"+mod+"'not found!\nInstall the python module '"+mod+"' and try again."
	exit()

MYDIR = path.dirname(path.realpath(__file__))
moduleDir.append(MYDIR+'/Modules')

#################
#   Functions   #
#################

from MyMods import wrap,URLSyntax,loadArray
from starter import checkForFiles,account

#################
#    Starter    #
#################

## Check to make sure all necessary files are there, then signs in.

showWarnings = True
checkForFiles()
reddit = praw.Reddit(user_agent= MYNAME+", an anonymous message relay hosted by /u/"+BOTMASTER+" for /r/ClosetSanta")
auth = OAuth2Util.OAuth2Util(reddit, print_log = True, configfile = MYDIR+"/MyFiles/oauth.ini")
auth.refresh(force=True)

## Variables that needed other functions to load before defining

SantaList = loadArray(MYDIR+"/SantaList.csv")
ACCOUNT = account()
PMLink = "https://www.reddit.com/message/compose/?to="+ACCOUNT+"&subject="+URLSyntax('Closet Santa message')+"&message="
botFlair=("\n\nHappy holidays from "+MYNAME+" and the /r/ClosetSanta mods!\n*****\n"
		"[Send mail to your gift recipient]("+PMLink+URLSyntax('From: Santa-san\n\nMessage: ')+") or "
		"[Send mail to your Closet Santa]("+PMLink+URLSyntax('To: Santa-san\n\nMessage: ')+")\n\n"
		"[^^I'm ^^open ^^source!](https://github.com/WolfgangAxel/ClosetSantaMessagingBot)")
		
## Import Reddit functions
import getPMs

## Begin monitoring

if __name__ == '__main__':
	greeting = "\n"+MYNAME+", reporting for duty!\n I will be using the account /u/"+ACCOUNT
	print "\n"
	wrap(greeting)
	print "From Santa link: "+PMLink+URLSyntax('From: Santa-san\n\nMessage: ')
	print "To Santa link: "+PMLink+URLSyntax('To: Santa-san\n\nMessage: ')
	while True:
		try:
			begin = time()
			getPMs.getPMs()
			end = time()
			if int(end-begin) < BOTFREQUENCY:
				sleep(BOTFREQUENCY-int(end-begin))
		except Exception as e:
			wrap("Looks like I'm having internet connection issues. I will try again in 5 minutes.\n\nError details: "+str(e.args))
			sleep(300)
