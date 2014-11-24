#!/usr/local/bin/python2.7


import xmlrpclib
import time

defaultStart='20000101T00:00:00'
defaultEnd='29991231T23:59:59'


class ISTag:

	def __init__(self, tagid, tagname, categoryid):
		self.tagid=tagid
		self.name=tagname
		self.categoryid=categoryid

class TagAppliedRecord:

	def __init__(self, contactID, contactFName, contactLName, contactEmail, tagName, tagID,tagtime):
		self.contactID=contactID
		self.fname=contactFName
		self.lname=contactLName
		self.email=contactEmail
		self.tagname=tagName
		self.tagid=tagID
		self.whenapplied=tagtime

class ISServer:


	def __init__(self, infusionsoftapp, infusionsoftAPIKey):
		self.infusionsoftapp=infusionsoftapp
		self.infusionsoftAPIKey=infusionsoftAPIKey
		self.appurl = "https://" + self.infusionsoftapp + ".infusionsoft.com:443/api/xmlrpc"
		self.connection = xmlrpclib.ServerProxy(self.appurl)

	def getTagCats(self):
		self.tagcats={}
		p=0
		while True:
			listOfDicts=self.connection.DataService.query(self.infusionsoftAPIKey, "ContactGroupCategory", 1000, p, {}, ['Id', 'CategoryName'], 'CategoryName',True)
			for eachCat in listOfDicts:
				self.tagcats[eachCat['Id']] = eachCat['CategoryName']
			if not(len(listOfDicts)==1000):
				break
			p=p+1

	def getAllTags(self):
		self.tags={}
		p=0
		while True:
			listOfDicts=self.connection.DataService.query(self.infusionsoftAPIKey, "ContactGroup", 1000,p,{},['Id',"GroupCategoryId","GroupName"],"GroupName", True )
			for eachtag in listOfDicts:
				self.tags[eachtag['Id']]=(ISTag(eachtag['Id'], eachtag['GroupName'], eachtag['GroupCategoryId']))
			if not(len(listOfDicts)==1000):
				break
			p=p+1

	def prep(self):
		self.getTagCats()
		self.getAllTags()


	def getContactsWithTag(self, startdate, enddate, tagID=303):
		records=[]
		sdate = time.strptime(startdate, '%Y%m%dT%H:%M:%S')
		edate = time.strptime(enddate, '%Y%m%dT%H:%M:%S')
		p=0
		while True:
			listOfDicts=self.connection.DataService.query(self.infusionsoftAPIKey, 'ContactGroupAssign', 1000,p,{'GroupId':tagID},['Contact.Email', 'Contact.FirstName', 'Contact.LastName', 'Contact.Id', 'DateCreated'],"Contact.Id",True)
			for eachApplication in listOfDicts:
				datetimeapplied = time.strptime(eachApplication['DateCreated'].value, '%Y%m%dT%H:%M:%S')
				if ((datetimeapplied>=sdate) and (datetimeapplied<=edate)):
					records.append(TagAppliedRecord(eachApplication['Contact.Id'],eachApplication['Contact.FirstName'],eachApplication['Contact.LastName'],eachApplication['Contact.Email'], self.tags[tagID].name, tagID, datetimeapplied))
			if not(len(listOfDicts)==1000):
				break
			p=p+1
		return records

	def verifyConnection(self):
		try:
			listOfDicts=self.connection.DataService.query(self.infusionsoftAPIKey, "User", 1000, 0,{},["Email"],"Email",True)
			return True
		except:
			return False

	def getCount(self, tableName, query):
		return self.connection.DataService.count(self.infusionsoftAPIKey, tableName, query)

	def createNewTag(self, newTagName):
		return self.connection.DataService.add(self.infusionsoftAPIKey, 'ContactGroup', {'GroupName':newTagName})

	def addTagToContact(self, contactID, tagID):
		self.connection.ContactService.addToGroup(self.infusionsoftAPIKey, contactID, tagID)

def prehead():
	pagehtml="""Content-type: text/html\n\n\n"""
	return pagehtml

def htmlHead():
	pagehtml = """
	<html>
		<head>
			<script src="//code.jquery.com/jquery-1.10.2.js"></script>
			<script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
			<script>
				$(function() {
					$( ".datepicker" ).datepicker();
				});
			</script>
		</head>
		<body>
	"""
	return pagehtml

def menu():
	pagehtml="""
	<div>
		<form method="POST">
			<input type="submit" name="logout" value="Logout">
			<input type="submit" name="btar" value="Better tag application report">
		</form>
	</div>
	"""
	return pagehtml

def selectionScreen(dictOfTags):
	pagehtml = """
			<form method="POST" action="">
				<input type="hidden" name="runbtar" value="run">
				<input type="text" class="datepicker" name="startdate">
				<input type="text" class="datepicker" name="enddate">
				<select size="10" multiple name="tags">
	"""
	tagids=dictOfTags.keys()
	taglist=[]
	for eachid in tagids:
		taglist.append((eachid,dictOfTags[eachid].name))
	taglist.sort(key=lambda val:val[1])
	for eachid in taglist:
		pagehtml = pagehtml + """
					<option value="%s">%s</option>
		""" %(str(eachid[0]), eachid[1])
	pagehtml = pagehtml + """
				</select>
				<input type="Submit" value="Search">
			</form>
	"""
	return pagehtml

def processInfo(postdata,server):
	contacts=[]
	taglist=[]
	if postdata.has_key('startdate'):
		smonth, sday, syear=postdata['startdate'].value.split('/')
		smonth = "%02d" %int(smonth)
		sday = "%02d" %int(sday)
		sstring=syear+smonth+sday+"T00:00:00"
	else:
		sstring="19000101T00:00:00"
	if postdata.has_key('enddate'):
		emonth, eday, eyear = postdata['enddate'].value.split('/')
		emonth = "%02d" %int(emonth)
		eday = "%02d" %int(eday)
		estring=eyear+emonth+eday+"T23:59:59"
	else:
		estring="30001231T23:59:59"
	if (type(postdata['tags'])==type(())):
		for eachtag in postdata['tags']:
			contacts.append(server.getContactsWithTag(sstring,estring,int(eachtag['tags'].value)))
			taglist.append(server.tags[int(eachtag['tags'].value)].name)
	else:
		contacts.append(server.getContactsWithTag(sstring,estring,int(postdata['tags'].value)))
		taglist.append(server.tags[int(postdata['tags'].value)].name)
	tagstring=''
	for eachtagname in taglist:
		tagstring = tagstring + eachtagname
	newtagstring=tagstring + """ applied from """ + sstring + " to " + estring
	pagehtml= """
			<form method="POST" action="">
				<div>
					Create the following tag and apply to all records: <input type='text' name='tagtoapply' value="%s"><br />
					<input type="submit" name="createandapplytag" value="Create and apply tag">
					<p>
						Note: this does not use an existing tag, even if you type the name of an existing tag in.  It will create
						a brand new tag, no matter what.
					</p>
				</div>
				<table>
					<tr>
						<td width="50">Id</td>
						<td width="200">Name</td>
						<td width="200">Email</td>
						<td width="200">Tag</td>
						<td width="200">Applied</td>
					</tr>
	""" %(newtagstring)
	for eachsearch in contacts:
		for eachrecord in eachsearch:
			recordURL="https://" + server.infusionsoftapp + ".infusionsoft.com/Contact/manageContact.jsp?view=edit&ID=" + str(eachrecord.contactID)
			pagehtml = pagehtml + """
					<tr>
						<td>
							<input type="text" name="update%s" value="%s" readonly>
						</td>
						<td><a href="%s">%s</a></td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
					</tr>
			""" %(str(eachrecord.contactID), str(eachrecord.contactID), recordURL, eachrecord.fname + " " + eachrecord.lname, eachrecord.email, eachrecord.tagname, time.strftime('%d%b%Y %H:%M:%S', eachrecord.whenapplied))
	pagehtml = pagehtml + """
				</table>
			</form>
	"""
	return pagehtml

def gatherInfo():
	pagehtml= """
			<form method="POST">
				<label for="appname">Appname</label>
				<input type="text" name="appname" id="appname">
				<label for="apikey">API Key</label>
				<input type="text" name="apikey" id="apikey">
				<input type='submit' name="submit" value="submit">
			</form>
	"""
	return pagehtml

def overview(server):
	totalTags = server.getCount('ContactGroup',{})
	totalContacts=server.getCount('Contact',{})
	pagehtml = """
			<table>
				<tr>
					<td>Total Tags</td>
					<td>%s</td>
				</tr>
				<tr>
					<td>Total Contacts</td>
					<td>%s</td>
				</tr>
			</table>""" %(str(totalTags), str(totalContacts))
	return pagehtml

def updateSeveralContacts(postdata, newTagId, server):
	allpostkeys=postdata.keys()
	for eachkey in allpostkeys:
		if (eachkey[:6]=="update"):
			cid=int(postdata[eachkey].value)
			server.addTagToContact(cid, newTagId)


def footer():
	pagehtml="""
		</body>
	</html>
	"""
	return pagehtml

