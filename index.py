#!/usr/local/bin/python2.7
import cgi
import cgitb

cgitb.enable()

import mysessions
import myfunc
import xmlrpclib

def sorting(postdata):
	mysessions.start()
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
		newTagId=server.createNewTag(postdata['tagtoapply'].value)
		myfunc.updateSeveralContacts(postdata, newTagId, server)
		pagehtml = myfunc.prehead() + myfunc.htmlHead() + myfunc.menu() + myfunc.overview(server) + myfunc.footer()
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