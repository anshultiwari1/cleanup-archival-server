# -*- coding: utf-8 -*-
"""
StereoD.
Author  : Anshul Tiwari
Date    : Sep 30, 2015

Description : This holds all the rpc.
"""
import datetime
from datetime import datetime, timedelta, date
import xmlrpclib
from models import *
import urllib2

from SimpleXMLRPCServer             import SimpleXMLRPCDispatcher

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher

from django.contrib.auth.models     import User
from django.contrib.auth.models     import Group
from django.core.mail               import send_mail
from django.db.models               import Q
from django.http                    import HttpResponse
from django.views.decorators.csrf 	import csrf_exempt
from django.core.files.base import ContentFile
import jsonrpclib
import json
import os, sys, glob
import shutil
import getpass
import types
from ast import literal_eval

# tactic server connection setup
sys.path.append("/nas/projects/development/productionTools/assetPublisher/tactic_modules")
targetFolders = ["/nas/projects/Tactic/bilal/sequences/", "/nas/projects/Tactic/bilal/render/"]
import queryClass as qClass
u = qClass.queryClass("bjTactic", "bilal")
import getTicket as serverSetup
userQuery = None
ticket = None

# set up environment
os.environ['TACTIC_APP_SERVER'] = "cherrypy"
os.environ['TACTIC_MODE'] = "production"

import tacticenv
#from pyasm.common import environment, config
tactic_install_dir = tacticenv.get_install_dir()
tactic_site_dir = tacticenv.get_site_dir()

sys.path.insert(0, "%s/src" % tactic_install_dir)
sys.path.insert(0, "%s/tactic_sites" % tactic_install_dir)
sys.path.insert(0, tactic_site_dir)
sys.path.insert(0, "%s/3rd_party/CherryPy" % tactic_install_dir)

from client.tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
# setup done

dispatcherJson = SimpleJSONRPCDispatcher(encoding=None)

# enable intospection, then map it to a different method, the system.listMethods call gets overwritten later
dispatcherJson.register_introspection_functions()

# Set true to log every rpc call to sentry
LOG_RPC = False

@csrf_exempt
def jsonrpc_handler(request):
  if len(request.POST):
    response = HttpResponse(mimetype="application/json")
    response.write(dispatcherJson._marshaled_dispatch(request.raw_post_data))
  else:
    return HttpResponse("No POST data, this url is for rpc calls only.")
  response['Content-length'] = str(len(response.content))
  return response

def tactic_login():
    ip="tactic"
    proj="bilal"
    uname = "anshul"
    passwd="anshul"
    serverSetup.setupClientServer(server_name=ip, project_code=proj, login=uname, password=passwd)
    userQuery = qClass.queryClass(ip, proj)
    ticket = userQuery.userLogin(uname, passwd)
if not ticket:
    tactic_login()
    print ticket

def getSequenceList():
  seqList = []
  for seq in u.server.query("{0}/seq".format(u.getProject()), filters=[]):
    seqList.append(seq['name'])
  seqList.sort()
  return seqList

def getSceneList(seq):
  seq_code = getSeqByName(seq)['code']
  scnList = []
  for scn in u.server.query("{0}/scn".format(u.getProject()), filters=[('seq_code', seq_code)]):
    scnList.append(scn['name'])
  scnList.sort()
  return scnList

def getShotList(seq, scn):
  seq_code = getSeqByName(seq)['code']
  scn_code = getScnByName(scn)['code']
  shotList = []
  for shot in u.getShtSObjectbyName(seq_code, scn_code):
    shotList.append(shot['name'])
  shotList.sort()
  return shotList

def getSeqByName(name):
  return u.server.query("{0}/seq".format(u.getProject()), filters = [('name', name)])[0]

def getScnByName(name):
  return u.server.query("{0}/scn".format(u.getProject()), filters = [('name', name)])[0]

def getShotByName(name):
  return u.server.query("vfx/shot", filters=[('name', name)])[0]

def getSeqByCode(code):
  return u.server.query("{0}/seq".format(u.getProject()), filters = [('code', code)])[0]

def getScnByCode(code):
  return u.server.query("{0}/scn".format(u.getProject()), filters = [('code', code)])[0]

def getShotByCode(code):
  return u.server.query("vfx/shot", filters=[('code', code)])[0]

def getUserAssignedShotList(user):
  userShotsList = []
  expr = ("@SOBJECT(sthpw/task['assigned', '%s']['project_code', '%s'])" % (user, u.getProject()))
  result = u.server.eval(expr, search_keys=[])
  for sh in result:
    if "SHOT" in sh['search_code']:
      shot = getShotByCode(sh['search_code'])
      userShotsList.append({'shot_code':shot['code'], 'sequence':getSeqByCode(shot['seq_code'])['name'], 'scene':getScnByCode(shot['scn_code'])['name'], 'shot':shot['name']})
  return sorted(userShotsList, key= lambda k:(k['sequence']))

def getUserAssignedAssetList(user):
  userAssetList = []
  expr = ("@SOBJECT(sthpw/task['assigned', '%s']['project_code', '%s'])" % (user, u.getProject()))
  assets = u.server.eval(expr, search_keys=[])
  for ast in assets:
    if "ASSET" in ast['search_code']:
      asset = u.server.eval("@SOBJECT(vfx/asset['code','%s'])" % (ast['search_code']))
      if asset:
        ele = {'asset_code':asset[0]['code'], 'name':asset[0]['name'], 'category':asset[0]['asset_category'], 'type':asset[0]['asset_type']}
        if ele not in userAssetList:
          #userAssetList.append({'asset_code':asset[0]['code'], 'name':asset[0]['name'], 'category':asset[0]['asset_category'], 'type':asset[0]['asset_type']})
          userAssetList.append(ele)
  if userAssetList:
    return sorted(userAssetList, key= lambda k:(k['name']))
  else:
    return userAssetList

def getShotFiles(feed):
  shotPath = '/nas/projects/Tactic/bilal/sequences/{0}/{1}/{2}_{3}/lighting/lighting/scenes/*_v[0-9]*'.format(feed['seq'],feed['scn'],feed['shot'],feed['shot_code'])
  shotFiles = [(fi, size_format(os.path.getsize(fi))) for fi in glob.glob(shotPath)]
  shotFiles.sort(key= lambda f:(os.path.getmtime(f[0])), reverse=True)
  return shotFiles

def getAssetFiles(feed):
  assetFiles = []
  assetPaths = ['/nas/projects/Tactic/bilal/asset/{0}_{1}/modeling/'.format(feed['asset'],feed['asset_code']), '/nas/projects/Tactic/bilal/asset/{0}_{1}/rigging/'.format(feed['asset'],feed['asset_code']), \
  '/nas/projects/Tactic/bilal/asset/{0}_{1}/texturing/'.format(feed['asset'],feed['asset_code'])]
  for pth in assetPaths:
    for sdir in os.listdir(pth):
      if glob.glob(pth+sdir+'/alembic/*_v[0-9]*'):
        fld = [(fi, size_format(os.path.getsize(fi))) for fi in glob.glob(pth+sdir+'/alembic/*_v[0-9]*')]
        fld.sort(reverse=True)
        assetFiles.append(fld)
      if glob.glob(pth+sdir+'/scenes/*_v[0-9]*'):
        fld = [(fi, size_format(os.path.getsize(fi))) for fi in glob.glob(pth+sdir+'/scenes/*_v[0-9]*')]
        fld.sort(reverse=True)
        assetFiles.append(fld)
  return assetFiles

def getStatusUpdate(infoPackage):
  print infoPackage
  for files in infoPackage:
    if files[1] == 'true':
      if not os.path.exists(os.path.join('/nas/projects/Tactic/bilal/render/temp', *files[0].split('/')[5:-1])):
        os.makedirs(os.path.join('/nas/projects/Tactic/bilal/render/temp', *files[0].split('/')[5:-1]))
      try:
        #os.rename(files[0], os.path.join('/nas/projects/Tactic/bilal/render/temp', *files[0].split('/')[5:]))
        shutil.copy2(files[0], os.path.join('/nas/projects/Tactic/bilal/render/temp', *files[0].split('/')[5:]))
      except Exception as e:
        print e
  return json.dumps(infoPackage, ensure_ascii=False)

def size_format(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for u in units:
        if size < 1024:  return '%0.2f %s' %(size, u)
        size /= 1024.0
    return '%0.2f %s' %(size, units[-1])


dispatcherJson.register_function(getSequenceList,			"getSequenceList")
dispatcherJson.register_function(getSceneList,				"getSceneList")
dispatcherJson.register_function(getShotList,				"getShotList")
dispatcherJson.register_function(getSeqByName,				"getSeqByName")
dispatcherJson.register_function(getScnByName,				"getScnByName")
dispatcherJson.register_function(getShotByName,				"getShotByName")
dispatcherJson.register_function(getSeqByCode,				"getSeqByCode")
dispatcherJson.register_function(getScnByCode,				"getScnByCode")
dispatcherJson.register_function(getShotByCode,				"getShotByCode")
dispatcherJson.register_function(getUserAssignedShotList,		"getUserAssignedShotList")
dispatcherJson.register_function(getUserAssignedAssetList,		"getUserAssignedAssetList")
dispatcherJson.register_function(getShotFiles,				"getShotFiles")
dispatcherJson.register_function(getAssetFiles,				"getAssetFiles")
dispatcherJson.register_function(getStatusUpdate,			"getStatusUpdate")

