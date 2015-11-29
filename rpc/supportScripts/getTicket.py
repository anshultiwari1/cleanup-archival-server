import os, sys
TOOLS_PATH=""

if os.environ.has_key("TOOLS_PATH"):
	TOOLS_PATH=os.environ["TOOLS_PATH"]
	if TOOLS_PATH not in sys.path and TOOLS_PATH != "" and TOOLS_PATH:
		sys.path.insert(0, TOOLS_PATH)
		
if not TOOLS_PATH and not os.path.exists(TOOLS_PATH):
	raise Exception("Please, set TOOLS_PATH Env variable")

from getProjectEnv import *
	
from tactic_client_lib import TacticServerStub

def setupClientServer(server_name="", project_code="", login="", password=""):
	
	if len(server_name) > 0 and len(project_code) > 0 and len(login) > 0 and len(password) > 0:
		server = TacticServerStub(setup=False)

		server.set_server(server_name)

		if os.name == "nt":
			dir = "C:/sthpw/etc"
		else:
			dir = "/tmp/sthpw/etc"
		if not os.path.exists(dir):
			os.makedirs(dir)

		filename = "%s.tacticrc" % login
		path = "%s/%s" % (dir,filename)

		# do the actual work
		ticket = server.get_ticket(login, password)
		print "Got ticket [%s] for [%s]" % (ticket, login)

		file = open(path, 'w')
		file.write("login=%s\n" % login)
		file.write("server=%s\n" % server_name)
		file.write("ticket=%s\n" % ticket)
		if project_code:
			file.write("project=%s\n" % project_code)

		file.close()
