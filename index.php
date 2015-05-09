#!/usr/local/bin/python2.7
import cgi
import cgitb

cgitb.enable()

import mysessions
import myfunc
import xmlrpclib

def sorting(postdata):
	mysessions.start()
	if (mysessions.SESSION.isset('counter')):
		mysessions.SESSION['counter'] = mysessions.SESSION['counter'] + 1
	else:
		mysessions.SESSION['counter'] = 0
	if not(mysessions.SESSION.isset('loggedin')):
		mysessions.SESSION['loggedin']=False
	if (postdata.has_key('logout')):
		
		mysessions.SESSION.set_expires(-1)
		print mysessions.SESSION.output()
		print myfunc.prehead()
		pagehtml = myfunc.htmlHead() + myfunc.gatherInfo() + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('apikey')):
		server=myfunc.ISServer(postdata['appname'].value, postdata['apikey'].value)
		if server.verifyConnection():
			mysessions.SESSION['loggedin']=True
			# mysessions.SESSION['server']=server
			mysessions.SESSION['appname'] = postdata['appname'].value
			mysessions.SESSION['apikey'] = postdata['apikey'].value
			mysessions.SESSION.set_expires(1)
			
			print mysessions.SESSION.output()
			print myfunc.prehead()
			pagehtml = myfunc.htmlHead() + myfunc.menu() + myfunc.overview(server) + myfunc.footer()
			print pagehtml
		else:
			
			mysessions.SESSION.set_expires(-1)
			print mysessions.SESSION.output()
			print myfunc.prehead()
			pagehtml = myfunc.htmlHead() + """<h2 color="red">Sorry, I could not log in. </h2>""" + myfunc.gatherInfo() + myfunc.footer()
			print pagehtml
	elif (postdata.has_key('btar')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu()
		server.prep()
		pagehtml = pagehtml + myfunc.selectionScreen(server.tags) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('runbtar')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		server.prep()
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.processInfo(postdata, server) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('createandapplytag')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		server.prep()
		if (postdata['neworold'].value == 'new'):
			newTagId=server.createNewTag(postdata['tagtoapply'].value)
		else:
			newTagId = int(postdata['tags'].value)
		myfunc.updateSeveralContacts(postdata, newTagId, server)
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.overview(server) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('rancon')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		server.prep()
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.randomContacts(postdata, server) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('rancon2')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		server.prep()
		pagehtml = myfunc.randomContacts2(postdata, server)
		if (pagehtml[:5]=="Error"):
			pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.overview(server, pagehtml) + myfunc.footer()
		else:
			pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + pagehtml + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('updateRanCon')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		server.prep()
		pagehtml = myfunc.updateRandomContacts(postdata, server)
		if (pagehtml[:5]=="Error"):
			pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.overview(server, pagehtml) + myfunc.footer()
		else:
			pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + pagehtml + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('alltags')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.tagsWithContacts(postdata, server) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('ordertest')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.purchasepage1() + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('goto2')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.purchasepage2(server) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('goto3')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.purchasepage3(postdata, server) + myfunc.footer()
		print pagehtml
	elif (postdata.has_key('goto4')):
		server = myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.purchasepage4(postdata, server) + myfunc.footer()
		print pagehtml

	elif (mysessions.SESSION['loggedin']==True):
		server=myfunc.ISServer(mysessions.SESSION['appname'], mysessions.SESSION['apikey'])
		pagehtml = myfunc.prehead()+myfunc.htmlHead() + myfunc.menu() + myfunc.overview(server) + myfunc.footer()
		print pagehtml
	else:
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.gatherInfo() + myfunc.footer()
		print pagehtml




if __name__ == '__main__':
	postdata=cgi.FieldStorage()
	sorting(postdata)