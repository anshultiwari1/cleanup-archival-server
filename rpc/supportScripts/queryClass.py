'''
    assetPublisher Tool Barajoun Entertainment copyright(c)
    Pipeline TD: Domingos Silva

    TACTIC QUERY MODULES
'''

import sys
import os
from pprint import pprint
import time
import glob, re, shutil

TOOLS_PATH=""

if os.environ.has_key("TOOLS_PATH"):
    TOOLS_PATH=os.environ["TOOLS_PATH"]
    if TOOLS_PATH not in sys.path and TOOLS_PATH != "" and TOOLS_PATH:
        sys.path.insert(0, TOOLS_PATH)

if not TOOLS_PATH and not os.path.exists(TOOLS_PATH):
    raise Exception("Please, set TOOLS_PATH Env variable")

from getProjectEnv import *

from tactic_client_lib import TacticServerStub


class queryClass(object):
    username=None
    ticket=None
    def __init__(self, server_IP, project, alias=ALIAS_PROJECT, repository=TACTIC_REPO):
        self.server_IP = server_IP
        self.project=project
        self.repository=repository
        self.server = TacticServerStub.get()
        ticket=self.server.get_login_ticket()
        self.server.set_ticket(ticket)
        self.server.set_server(self.server_IP)
        self.server.set_project(project)
        self.alias=alias

        self.iconPath=None
        self.iconDirnaming=None

    def getProject(self):
        return self.project

    def setRepository(self, repository):
        self.repository=repository

    def userLogin(self, username, password):
        self.username=username
        self.password=password
        self.ticket = self.server.get_ticket(self.username, self.password)
        self.server.set_ticket(self.ticket)
        #self.ticket = self.server.get_ticket("apache", "apache")
        #self.server.set_ticket(self.ticket)
        return self.ticket

    #GET TASK FROM SHOT FROM CURRENT PROJECT SET
    def getShotTask(self, shotCode):
        #expr = ("@SOBJECT(%s/shot.sthpw/task['search_code','EQ','%s'])" % (self.project, shotCode))
        expr = ("@SOBJECT(%s/shot.sthpw/task['search_code','EQ','%s'])" % (self.alias, shotCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #shottask=getShotTask("shot01")


    #GET ASSET BY CODE FROM CURRENT PROJECT SET
    def getAssetTask(self, assetCode):
        #expr = ("@SOBJECT(%s/asset.sthpw/task['search_code','EQ','%s'])" % (self.project,assetCode))
        expr = ("@SOBJECT(%s/asset.sthpw/task['search_code','EQ','%s'])" % (self.alias, assetCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #thisAsset=getAssetTask("asset01")


    #GET ALL USER TASK ASSIGNED BY SHOT CODE FROM CURRENT PROJECT SET
    def getUsersShotTaskAssigned(self, shotCode):
        expr = ("@GET(%s/shot.sthpw/task['begin']['search_code','EQ','%s']['or'].assigned)" % (self.project, shotCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #shotUsers=getUsersShotTaskAssigned("shot01")


    #GET ALL USERS ASSIGNED  TO A TASK
    '''
    def getTaskAssignedUsers(self, search_code, process, context):
        expr = ("@GET(sthpw/task['project_code', '%s']['search_code', '%s']['process', '%s']['context', '%s'].assigned)" % (self.project, search_code, process, context))
        expr1 = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code', '%s']['process', '%s']['context', '%s'])" % (self.project, search_code, process, context))
        result = self.server.eval(expr, search_keys=[] )
        result1 = self.server.eval(expr1, search_keys=[] )
        return result1, result
    #shotUsers=getUsersAssetTaskAssigned("asset02")
    '''
    #GET ALL USERS ASSIGNED  TO A TASK
    def getTaskAssignedUsers(self, search_code, process, context, order_bys=[]):
        expr = ("@GET(sthpw/task['project_code', '%s']['search_code', '%s']['process', '%s']['context', '%s'].assigned)" % (self.project, search_code, process, context))
        result = self.server.eval(expr, search_keys=[] )

        filters = []
        filters.append(("project_code", self.project))
        filters.append(("search_code", search_code))
        filters.append(("process", process))
        filters.append(("context", context))

        result1=self.server.query("sthpw/task", filters=filters, order_bys=order_bys)
        return result1, result


    #GET CURRENT USER LOGIN
    def getCurrentUser(self):
        expr = "@SOBJECT(sthpw/login['login',$LOGIN])"
        result = self.server.eval(expr, search_keys=[] )
        return result
    #user=getCurrentUser()

    #GET CURRENT USER LOGIN
    def getUsersAssignedToTask(self):
        expr = "@SOBJECT(sthpw/login['login',$LOGIN])"
        result = self.server.eval(expr, search_keys=[] )
        return result
    #user=getCurrentUser()

    #GET CURRENT USER SHOT TASK  FROM CURRENT PROJECT SET
    def getCurrentUserShotTask(self):
        #expr = ("@SOBJECT(%s/shot.sthpw/task['assigned', '%s'])" % (self.project, self.username))
        expr = ("@SOBJECT(%/shot.sthpw/task['assigned', '%s']['project_code', '%s'])" % (self.alias, self.username, self.project))
        result = self.server.eval(expr, search_keys=[])
        return result
    #userShotTask=getUserShotTask("arif")

    #GET USER SHOT TASK  FROM CURRENT PROJECT SET
    def getUserShotTask(self, user):
        #expr = ("@SOBJECT(%s/shot/task['assigned', '%s'])" % (self.project, user))
        expr = ("@SOBJECT(%s/shot.sthpw/task['assigned', '%s']['project_code', '%s'])" % (self.alias, user, self.project))
        result = self.server.eval(expr, search_keys=[])
        return result
    #userShotTask=getUserShotTask("arif")


    #GET SHOT BY SHOT CODE  FROM CURRENT PROJECT SET
    def getShotByCode(self, shotCode):
        #expr = ("@SOBJECT(%s/shot['code','%s'])" % (self.project, shotCode))
        expr = ("@SOBJECT(%s/shot['code','%s'])" % (self.alias, shotCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #shot=getShotByCode("shot01")

    def getAssetByCode(self, assetCode):
        expr = ("@SOBJECT(%s/asset['code','%s'])" % (self.alias, assetCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getAssetByCode("asset02")

    def getTaskByCode(self, taskCode):
        filters = []
        filters.append(("project_code", self.project))
        filters.append(("code", taskCode))

        result=self.server.query("sthpw/task", filters=filters)
        return result
    #task=getTaskByCode("task02")

    #GET TASKS BY SHOT CODE FROM CURRENT PROJECT SET
    def getTaskByShotByCode(self, shotCode):
        #expr = ("@SOBJECT(%s/shot['code','%s'].sthpw/task)" % (self.project, shotCode))
        expr = ("@SOBJECT(%s/shot['code','%s'].sthpw/task)" % (self.alias, shotCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByShotByCode("shot01")

    #GET TASKS BY SHOT CODE FROM CURRENT PROJECT SET
    def getCurrentUserTaskByShotByCode(self, shotCode, status=None):
        #expr = ("@SOBJECT(%s/shot['code','%s'].sthpw/task)" % (self.project, shotCode))
        if status is not None:
            expr = ("@SOBJECT(%s/shot['code','%s'].sthpw/task['assigned', '%s']['status', '%s']['project_code', '%s'])" % (self.alias, shotCode, self.username, status, self.project))
        else:
            expr = ("@SOBJECT(%s/shot['code','%s'].sthpw/task['assigned', '%s']['project_code', '%s'])" % (self.alias, shotCode, self.username, self.project))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByShotByCode("shot01")


    #GET ASSETS IN A SHOT BY SHOT CODE FROM CURRENT PROJECT SET
    def getAssetInShot(self, shotCode):
        #expr = ("@SOBJECT(%s/asset_in_shot['shot_code','shot01'])" % self.project)
        expr = ("@SOBJECT(%s/asset_in_shot['shot_code','%s']['project_code', '%s'])" % (self.alias, shotCode, self.project))
        result = self.server.eval(expr, search_keys=[])
        return result
    #assets=getAssetInShot("shot01")

    #GET ASSETS IN A SHOT BY SHOT CODE FROM CURRENT PROJECT SET
    def getAssetSObjectInShot(self, shotCode):
        results=self.getAssetInShot(shotCode)
        sobjs=[]
        for res in results:
            #expr = ("@SOBJECT(%s/asset_in_shot['shot_code','shot01'])" % self.project)
            expr = ("@SOBJECT(%s/asset['code','%s'])" % (self.alias, res["asset_code"]))
            result = self.server.eval(expr, search_keys=[])
            sobjs.extend(result)
        return sobjs
    #assets=getAssetInShot("shot01")


    #GET ASSETS IN A SEQ
    def getAssetInScene(self, scnCode, category="", status="Approved"):
        expr = ("@SOBJECT(%s/asset_in_scn['scn_code','%s'])" % (self.project, scnCode))
        result = self.server.eval(expr, search_keys=[])

        tasksSObjetcs=[]

        #print result

        for res in result:
            assetCode = res['asset_code']
            assetSobj=self.getAssetByCode(assetCode)

            if len(assetSobj) > 0:
                if category in assetSobj[0]['asset_category']:
                    tsobjs=self.getTasksByAssetCodeAndStatus(assetCode, status)
                    tasksSObjetcs.extend(tsobjs)

        return tasksSObjetcs

    #GET PROJECT TASK BY SEARCH_TYPE (ASSET OR SHOT)
    def getProjectTasksBySearchType(self, search_type="%s/asset" % ALIAS_PROJECT, status=""):

        filters = []
        filters.append(("project_code", self.project))
        filters.append(("search_type", "%s?project=%s" % (search_type, self.project)))

        if status != "":
            filters.append(("status", status))

        tasks=self.server.query("sthpw/task", filters=filters)

        return tasks

    def getShotReviewList(self, status="In Progress"):
        result={}
        tasks=self.getProjectTasksBySearchType(search_type="%s/shot" % ALIAS_PROJECT, status=status)
        for task in tasks:
            try:
                code=task["code"]
                res=self.getShotSceneSequenceName(task)
                res["context"]=task["context"]
                res["process"]=task["process"]

                result[code]=res
            except: pass

        return result

    def getAssetReviewList(self, status="In Progress"):
        result={}
        tasks=self.getProjectTasksBySearchType(search_type="%s/asset" % CUR_PROJECT, status=status)
        for task in tasks:
            try:
                code=task["code"]
                res=self.getShotSceneSequenceName(task)
                res["context"]=task["context"]
                res["process"]=task["process"]

                result[code]=res
            except: pass

        return result

    #GET SCENE SHOT
    def getSceneShotByScnCode(self, scnCode):
        filters = []
        filters.append(("pipeline_code", "%s/shot" % self.project))
        filters.append(("scn_code", scnCode))
        shots=self.server.query("%s/shot" % ALIAS_PROJECT, filters=filters)

        return shots

    #GET SHOT TASK BY PORCESS AND CONTEXT
    def getShotTaskByProcessAndContext(self, search_code, process, context="", status="Approved", asset_name=None):

        filters = []
        filters.append(("project_code", self.project))
        filters.append(("search_code", search_code))
        filters.append(("process", process))
        if context != "":
            filters.append(("context", context))
        if status:
            filters.append(("status", status))
        if asset_name:
            filters.append(("asset_name", asset_name))
        tasks=self.server.query("sthpw/task", filters=filters)

        return tasks

    #GET SCENE TASK BY PROCESS AND CONTEXT
    def getSceneTasksByProcessAndContext(self, scnCode, process, context="", status="Approved"):
        shots=self.getSceneShotByScnCode(scnCode)
        tasks=[]
        for shot in shots:
            res=[]
            if context != "":
                res=self.getShotTaskByProcessAndContext(shot['code'], process, context, status=status)
            else:
                res=self.getShotTaskByProcessAndContext(shot['code'], process, status=status)
            if res:
                tasks.extend(res)

        return tasks


    #GET Task ASSET SOBJECT IN DYNAMIC ASSET BY ASSET CODE
    def getSObjectsTaskAssetInShot(self, shotCode, process="", status=""):
        #expr = ("@SOBJECT(%s/asset_in_shot['shot_code','shot01'])" % self.project)
        expr = ("@SOBJECT(%s/asset_in_shot['shot_code','%s'])" % (self.alias, shotCode))
        result = self.server.eval(expr, search_keys=[])
        tasksSObjetcs=[]

        for res in result:
            assetCode = res['asset_code']
            assetSobj=self.getAssetByCode(assetCode)
            sobject=[]
            if process != "":
                sobjects=self.getTasksByAssetCodeAndProcess(assetCode, process)
                if len(sobjects) == 0 and process == "asset" and "ASSET" in assetCode:
                    assetSobj=self.getAssetByCode(assetCode)
                    if len(assetSobj) > 0:
                        self.server.create_task(assetSobj[0]["__search_key__"], process=process, subcontext=process)
                        sobjects=self.getTasksByAssetCodeAndProcessAndStatus(assetCode, process, status)

                for sobj in sobjects:
                    deptsobjs=self.getTasksDependencesFromPipelineInfo(sobj, status=status)
                    tasksSObjetcs.extend(deptsobjs["src"])
                    tasksSObjetcs.extend(deptsobjs["dst"])
            else:
                #tsobjs=self.getTasksByAssetCode(assetCode)
                tsobjs=self.getTasksByAssetCodeAndStatus(assetCode, status)
                for task in tsobjs:
                    ctask=self.getTaskSObjectMultiAssigned(task)
                    if ctask not in tasksSObjetcs:
                        tasksSObjetcs.append(ctask)
                #tasksSObjetcs.extend(tsobjs)

        return tasksSObjetcs
    #assets=getAssetInShot("shot01")

    #GET Task ASSET SOBJECT IN A SHOT BY SHOT CODE FROM CURRENT PROJECT SET
    def getSObjectsTaskAssetInDynAsset(self, assetCode, process="", status=""):
        #expr = ("@SOBJECT(%s/asset_in_shot['shot_code','shot01'])" % self.project)
        expr = ("@SOBJECT(%s/asset_in_dynamic_asset['asset_code','%s'])" % (self.project, assetCode))
        result = self.server.eval(expr, search_keys=[])
        assetSObjetcs=[]
        for res in result:
            assetCode = res['asset_static_code']
            sobject=[]
            if process != "":
                sobjects=self.getTasksByAssetCodeAndProcess(assetCode, process)
                if len(sobjects) == 0 and process == "dynamicAsset" and "ASSET" in assetCode:
                    assetSobj=self.getAssetByCode(assetCode)
                    if len(assetSobj) > 0:
                        self.server.create_task(assetSobj[0]["__search_key__"], process=process, subcontext=process)
                        sobjects=self.getTasksByAssetCodeAndProcessAndStatus(assetCode, process, status)

                #sobject=self.getTaskByAssetCodeAndContex(assetCode, process)
            else:
                sobject=self.getTasksByAssetCodeAndStatus(assetCode, status)
            assetSObjetcs.extend(sobject)
        return assetSObjetcs
    #assets=getSObjectsTaskAssetInDynAsset("ASSET00000119", "asset")


    #GET ASSET IN A SHOT BY ASSET CODE AND SHOT CODE FROM CURRENT PROJECT SET
    def getAssetByCodeInShot(self, shotCode, assetCode):
        #expr = ("@SOBJECT(%s/asset_in_shot['shot_code','%s']['asset_code', '%s'])" % (self.project, shotCode, assetCode))
        expr = ("@SOBJECT(%s/asset_in_shot['shot_code','%s']['asset_code', '%s'])" % (self.alias, shotCode, assetCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #asset=getAssetByCodeInShot("shot01", "asset01")


    #GET CURRENT PROJECT TASKS COUNT BY PROJECT CODE
    def getProjectTaskCount(self):
        expr = ("@COUNT(sthpw/task['project_code', '%s'])" % self.project)
        result = self.server.eval(expr, search_keys=[] )
        return result
    #taskCount=getProjectTaskCount("tactic_test")


    #GET CURRENT PROJECT TASKS BY PROJECT CODE
    def getCurrentProjectTask(self):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s'])" % self.project)
        result = self.server.eval(expr, search_keys=[] )
        return result
    #tasks=getProjectTask("tactic_test")

    #GET PROJECT TASKS BY PROJECT CODE
    def getProjectTask(self, projCode):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s'])" % projCode)
        result = self.server.eval(expr, search_keys=[] )
        return result
    #tasks=getProjectTask("tactic_test")

    #GET CURRENT PROJECT TASKS BY PROJECT CODE
    def getTaskBySearchcodeContext(self, search_code, context):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code', '%s']['context', '%s'])" % (self.project, search_code, context))
        result = self.server.eval(expr, search_keys=[] )
        return result
    #tasks=getProjectTask("tactic_test")


    #GET CURRENT USER TASKS BY PROJECT CODE AND USER NAME FROM CURRENT PROJECT SET
    def getCurrentUserTasks(self, status=None):
        if status is not None:
            print "I'm here"
            expr = ("@SOBJECT(sthpw/task['project_code', '%s']['assigned', '%s']['status', '%s'])" % (self.project, self.username, status))
        else:
            expr = ("@SOBJECT(sthpw/task['project_code', '%s']['assigned', '%s'])" % (self.project, self.username))
        result = self.server.eval(expr, search_keys=[] )

        if len(result) == 0:
            if status is not None:
                expr = ("@SOBJECT(sthpw/task['project_code', '%s']['supervisor', '%s']['status', '%s'])" % (self.project, self.username, status))
            else:
                expr = ("@SOBJECT(sthpw/task['project_code', '%s']['supervisor', '%s'])" % (self.project, self.username))
            result = self.server.eval(expr, search_keys=[] )

        return result
    #tasks=getCurrentUserTasks()

    def getCurrentUserTasksByStatus(self, statusCode):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['assigned', '%s']['status', '%s'])" % (self.project, self.username, statusCode))
        result = self.server.eval(expr, search_keys=[] )
        return result
    #tasks=getCurrentUserTasksByStatus("In Progress")

    #GET USER TASKS BY PROJECT CODE AND USER NAME FROM A PROJECT CODE
    def getUserTasks(self, projCode, user):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['assigned', '%s'])" % (projCode, user))
        result = self.server.eval(expr, search_keys=[] )
        return result
    #tasks=getUserTasks("tactic_test", "arif")

    def getUserTasksBySearchKey(self, search_key):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['assigned', '%s'])" % (self.project, self.username))
        result = self.server.eval(expr, search_keys=[search_key])
        return result[0]
    #tasks=getUserTasks("tactic_test", "arif")

    #GET CURRENT PROJECT ASSETS BY PROJECT CODE
    def getCurrentProjectAssets(self):
        expr = ("@SOBJECT(%s/asset)" % self.project)
        result = self.server.eval(expr, search_keys=[] )
        return result
    #assets=getProjectAssets("vfx")

    #GET PROJECT ASSETS BY PROJECT CODE
    def getProjectAssets(self, projCode):
        expr = ("@SOBJECT(%s/asset)" % projCode)
        result = self.server.eval(expr, search_keys=[] )
        return result
    #assets=getProjectAssets("vfx")

    #GET TASK BY ASSET CODE FROM CURRENT PROJECT SET
    def getTaskByAssetCode(self, assetCode):
        #expr = ("@SOBJECT(%s/asset['code','%s'].sthpw/task)" % (self.project, assetCode))
        expr = ("@SOBJECT(%s/asset['code','%s'].sthpw/task)" % (self.alias, assetCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByAssetCode("asset01")

    #GET TASK BY ASSET CODE FROM CURRENT PROJECT SET
    def getCurrentUserTaskByAssetCode(self, assetCode):
        #expr = ("@SOBJECT(%s/asset['code','%s'].sthpw/task)" % (self.project, assetCode))
        expr = ("@SOBJECT(%s/asset['code','%s'].sthpw/task['assigned', '%s'])" % (self.alias, assetCode, self.username))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByAssetCode("asset01")

    #GET TASK BY ASSET CODE FROM CURRENT PROJECT SET
    def getTaskByProjectCodeAndAssetCode(self, projCode, assetCode):
        expr = ("@SOBJECT(%s/asset['code','%s'].sthpw/task)" % (projCode, assetCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByAssetCode("tactic_test","asset01")

    #GET TASK BY ASSET CODE AND CONTEXT FROM CURRENT PROJECT SET
    def getTaskByAssetCodeAndContex(self, assetCode, context):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code','%s']['context', '%s'])" % (self.project, assetCode, context))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByAssetCodeAndContex("asset02", "model")

    def getTasksByAssetCodeAndContext(self, assetCode, context):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code','%s']['context', '%s'])" % (self.project, assetCode, context))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByAssetCodeAndContex("asset02", "model")

    def getTasksByAssetCode(self, assetCode):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code','%s'])" % (self.project, assetCode))
        result = self.server.eval(expr, search_keys=[])
        return result
    #task=getTaskByAssetCodeAndContex("asset02", "model")

    #GET TASKS BY ASSET CODE AND STATUS FROM CURRENT PROJECT SET
    def getTasksByAssetCodeAndStatus(self, assetCode, status):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code','%s']['status', '%s'])" % (self.project, assetCode, status))
        result = self.server.eval(expr, search_keys=[])
        return result
    #tasks=getTasksByAssetCodeAndStatus("asset02", "Approved")

    #GET TASKS BY ASSET CODE AND STATUS FROM CURRENT PROJECT SET
    def getTasksByAssetCodeAndProcessAndStatus(self, assetCode, process, status):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code','%s']['process', '%s']['status', '%s'])" % (self.project, assetCode, process, status))
        result = self.server.eval(expr, search_keys=[])
        return result
    #tasks=getTasksByAssetCodeAndStatus("asset02", "Approved")

    #GET TASKS BY ASSET CODE AND PROCESS FROM CURRENT PROJECT SET
    def getTasksByAssetCodeAndProcess(self, assetCode, process):
        expr = ("@SOBJECT(sthpw/task['project_code', '%s']['search_code','%s']['process', '%s'])" % (self.project, assetCode, process))
        result = self.server.eval(expr, search_keys=[])
        return result
    #tasks=getTasksByAssetCodeAndProcess("asset02", "model")

    #GET FILES FROM FROM SNAPSHOT CODE CURRENT PROJECT SET
    def getAllFileSObjectFromSnapshot(self, snapshot_code):
        expr = ("@SOBJECT(sthpw/file['project_code', '%s']['snapshot_code', '%s'])" % (self.project, snapshot_code))
        result = self.server.eval(expr, search_keys=[])
        return result
    #file=getFileByName("umayyaAdult_mdl")

    #GET FILES FROM FROM SNAPSHOT CODE CURRENT PROJECT SET
    def getFileSObjectByName(self, snapshot_code, basename):
        expr = ("@SOBJECT(sthpw/file['project_code', '%s']['snapshot_code', '%s']['file_name', '%s'])" % (self.project, snapshot_code, basename))
        result = self.server.eval(expr, search_keys=[])
        return result
    #file=getFileByName("umayyaAdult_mdl")

    #GET FILES BY TYPE FROM SNAPSHOT CODE CURRENT PROJECT SET
    def getFileSObjectByType(self, snapshot_code, type):
        expr = ("@SOBJECT(sthpw/file['project_code', '%s']['snapshot_code', '%s']['type', '%s'])" % (self.project, snapshot_code, type))
        result = self.server.eval(expr, search_keys=[])
        return result
    #file=getFileByName("umayyaAdult_mdl")

    #GET FILES BY TYPE FROM SNAPSHOT CODE CURRENT PROJECT SET
    def getSnapshotSObjectByCode(self, snapshot_code):
        expr = ("@SOBJECT(sthpw/snapshot['project_code', '%s']['code', '%s'])" % (self.project, snapshot_code))
        result = self.server.eval(expr, search_keys=[])
        return result
    #file=getFileByName("umayyaAdult_mdl")

    def getScnCodeByScnName(self, scn_name, seq_code=None):
        expr = ("@SOBJECT(%s/scn['name','%s']['s_status', 'is', 'NULL'])" % (self.project, scn_name))
        if seq_code:
            expr = ("@SOBJECT(%s/scn['name','%s']['seq_code','%s']['s_status', 'is', 'NULL'])" % (self.project, scn_name, seq_code))

        result = self.server.eval(expr, search_keys=[])
        if len(result) > 0:
            return result[0]["code"]
        return None
    #scnCode=getScnCodeByScnName("scn22")

    def getScnNameBySeqCode(self, seq_code):
        expr = ("@SOBJECT(%s/scn['seq_code','%s']['s_status', 'is', 'NULL'])" % (self.project, seq_code))

        result = self.server.eval(expr, search_keys=[])
        return result

    def getShNameBySeqCode(self, seq_code):
        expr = ("@SOBJECT(%s/shot['seq_code','%s']['s_status', 'is', 'NULL'])" % (self.alias, seq_code))

        result = self.server.eval(expr, search_keys=[])
        return result

    def getSeqCodeBySeqName(self, seq_name):
        expr = ("@SOBJECT(%s/seq['name','%s']['s_status', 'is', 'NULL'])" % (self.project, seq_name))
        result = self.server.eval(expr, search_keys=[])
        if len(result) > 0:
            return result[0]["code"]
        return None
    #seqCde=getSeqCodeBySeqName("seq08")

    def getShCodeByShNameScnCodeAndSeqCode(self, sh_name, scn_code, seq_code, sobj=False):
        print sh_name, scn_code, seq_code, self.alias
        expr = ("@SOBJECT(%s/shot['name','%s']['scn_code','%s']['seq_code','%s']['s_status', 'is', 'NULL'])" % (self.alias, sh_name, scn_code, seq_code))
        result = self.server.eval(expr, search_keys=[])

        if len(result) > 0:
            if sobj:
                return result[0]
            else:
                return result[0]["code"]

        return None
    #seqCde=getShCodeByShNameScnCodeAndSeqCode("sh008", "SCN00000006", "SEQ0000012")

    def isSObjectSrcConnection(self, srcSobject, dstSobject):
        '''
            Check if two SObject is connected
            srcSobject - the source Sobject
            dstSobject - the destination Sobject
            return 0 if is source, 1 if is destination and -1 if is not connected
        '''
        srcID = srcSobject['id']
        dstID = dstSobject['id']
        print srcSobject['context'], dstSobject['context'], srcID, dstID
        expr = ("@SOBJECT(sthpw/connection['project_code', '%s']['src_search_id', '%s']['dst_search_id', '%s'])" % (self.project, srcID, dstID))
        result = self.server.eval(expr, search_keys=[] )
        if len(result) > 0:
            return 0
        else:
            #print "Here DST"
            expr = ("@SOBJECT(sthpw/connection['project_code', '%s']['src_search_id', '%s']['dst_search_id', '%s'])" % (self.project, dstID, srcID))
            result = self.server.eval(expr, search_keys=[])
            if len(result) > 0:
                return 1

        return -1

    def getSObjectConnection(self, srcSobject, isSrc=True):
        '''
            Get SObject connection from given SObject

            srcSobject - the source Sobject to get the connection associated
            return the list of connection SObjects that cointain the srcObject
        '''
        srcID = srcSobject['id']
        sobjects = {}

        if isSrc:
            expr = ("@SOBJECT(sthpw/connection['project_code', '%s']['src_search_id', '%s']['context', 'out_connection'])" % (self.project, srcID))
            result = self.server.eval(expr, search_keys=[])
            sobjects['dst'] = result

            expr = ("@SOBJECT(sthpw/connection['project_code', '%s']['dst_search_id', '%s']['context', 'in_connection'])" % (self.project, srcID))
            result = self.server.eval(expr, search_keys=[] )
            sobjects['src'] = result
        else:
            expr = ("@SOBJECT(sthpw/connection['project_code', '%s']['dst_search_id', '%s']['context', 'out_connection'])" % (self.project, srcID))
            result = self.server.eval(expr, search_keys=[])
            sobjects['src'] = result

            expr = ("@SOBJECT(sthpw/connection['project_code', '%s']['src_search_id', '%s']['context', 'in_connection'])" % (self.project, srcID))
            result = self.server.eval(expr, search_keys=[] )
            sobjects['dst'] = result

        return sobjects

    def getTaskSObjectsFromConnection(self, thisSobject, isSrc=False):
        sobjects = []
        connections = self.getSObjectConnection(thisSobject, isSrc)

        for key in connections.keys():
            for conn in connections[key]:
                if conn['context'] == "in_connection" and isSrc == False:
                    expr = ("@SOBJECT(sthpw/task['project_code', '%s']['id', '%s'])" % (self.project, conn['dst_search_id']))
                    result = self.server.eval(expr, search_keys=[])
                    sobjects.extend(result)
                elif conn['context'] == "out_connection" and isSrc == True:
                    expr = ("@SOBJECT(sthpw/task['project_code', '%s']['id', '%s'])" % (self.project, conn['src_search_id']))
                    result = self.server.eval(expr, search_keys=[])
                    sobjects.extend(result)

        return sobjects

    def getPipelineDependencesFromXml(self, search_key):
        '''
            Get the pipeline xml defination by given asset/shot search_key

            search_key - the asset/shot search_key
            return the connections directionary with from and to process
        '''
        result = self.server.get_pipeline_xml_info(search_key)
        xmls = result['xml']
        print result
        connections = []
        for line in xmls.split('\n'):
            if "connect" in line:
                #print line
                connection={}
                tokens = line.split()
                fromTokens = tokens[1].split('"')
                toTokens = tokens[2].split('"')
                connection['from'] = fromTokens[1]
                connection['to'] = toTokens[1]
                connections.append(connection)
        return connections

    def getPipelineInfo(self, search_key, process):
        '''
            Get the pipeline defination by given asset/shot search_key and process

            search_key - the asset/shot search_key
            process - the context of connection
            return the dictionary of connection
        '''
        result = self.server.get_pipeline_processes_info(search_key, recurse=False, related_process=process)
        return result

    def getTasksDependencesFromPipelineInfo(self, thisSOBJECT, status=""):
        sobject1=self.server.get_by_code(thisSOBJECT["search_type"], thisSOBJECT["search_code"])
        connection=self.getPipelineInfo(sobject1["__search_key__"], thisSOBJECT["process"])

        deptasks={}
        deptasks['src']=[]
        deptasks['dst']=[]
        skipTask=[]

        process=thisSOBJECT["process"]
        sub_task=self.getTasksByAssetCodeAndProcess(thisSOBJECT["search_code"], process)

        for ttask in sub_task:
            if ttask['code'] != thisSOBJECT['code'] and ttask['context'] != thisSOBJECT['context']:
                deptasks['src'].append(ttask)

            #else:
            #   print ttask['context']

        if len(connection['input_processes']) > 0:
            for i in range(len(connection['input_processes'])):
                in_tasks=self.getTasksByAssetCodeAndProcess(thisSOBJECT["search_code"], connection['input_processes'][i])
                for itask in in_tasks:
                    if status == "":
                        status=itask['status']

                    if itask['code'] != thisSOBJECT['code']:
                        #print itask['context']
                        sobjects, assignedUsers=self.getTaskAssignedUsers(itask['search_code'], itask['process'], itask['context'])
                        if len(sobjects) > 1:
                            tsobject=self.getTaskSObjectMultiAssigned(itask)

                            if tsobject['code'] not in skipTask:
                                deptasks['src'].append(tsobject)
                            skipTask.append(tsobject['code'])
                        else:
                            if itask['code'] not in skipTask:
                                deptasks['src'].append(itask)
                        skipTask.append(itask['code'])
                    else:
                        skipTask.append(itask['code'])


        if len(connection['output_processes']) > 0:
            for i in range(len(connection['output_processes'])):
                out_tasks=self.getTasksByAssetCodeAndProcess(thisSOBJECT["search_code"], connection['output_processes'][i])
                for otask in out_tasks:
                    if status == "":
                        status=otask['status']

                    if otask['code'] != thisSOBJECT['code']:
                        sobjects, assignedUsers=self.getTaskAssignedUsers(otask['search_code'], otask['process'], otask['context'])
                        if len(sobjects) > 1:
                            tsobject=self.getTaskSObjectMultiAssigned(otask)
                            if tsobject['code'] not in skipTask:
                                deptasks['dst'].append(tsobject)
                            skipTask.append(tsobject['code'])
                        else:
                            if otask['code'] not in skipTask:
                                deptasks['dst'].append(otask)
                        skipTask.append(otask['code'])
                    else:
                        skipTask.append(otask['code'])

        return deptasks


    def getTaskDependences(self, thisSOBJECT):
        '''
            Get connected SObjects

            tacticSOBJECT - the soruce SObject to get the connected SObject to it
            return dictionary of source and destination Sobjects
        '''
        sobjects = {}
        result = self.server.get_connected_sobjects(thisSOBJECT, context='in_connection')
        sobjects['dst'] = result

        result = self.server.get_connected_sobjects(thisSOBJECT, context='out_connection')
        sobjects['src'] = result


        return sobjects


    '''def updateSObjectFilename(self, fileSObject, basename):
        search_key = fileSObject['__search_key__']
        data = {
            'file_name': '%s' % basename
        }
        result = self.server.update(search_key, data)
        return result'''

    def getParentSobjects(self, tasks):
        sKeys=[]
        pSobjects=[]
        for task in tasks:
            sk=self.server.build_search_key(task["search_type"], task["search_code"])
            sKeys.append(sk)

        if len(sKeys) > 0:
            pSobjects = self.server.get_by_search_key(sKeys)
        return pSobjects

    def getShotSceneSequenceName(self, thisSOBJECT):
        sobject1=self.server.get_by_code(thisSOBJECT["search_type"], thisSOBJECT["search_code"])

        task_code=thisSOBJECT['code']
        proj_code=thisSOBJECT['project_code']
        parent_code=sobject1['code']

        sh_name=""
        sc_name=""
        seq_name=""

        if "SHOT" in parent_code:
            sh_name=sobject1['name']

            sch_type="%s/scn"  % CUR_PROJECT
            search_type=self.server.build_search_type(sch_type, project_code=proj_code)
            sc_sobject=self.server.get_by_code(search_type, sobject1["scn_code"])
            sc_code=sc_sobject['code']

            if "SCN" in sc_code:
                sc_name=sc_sobject['name']

                sch_type="%s/seq" % CUR_PROJECT
                search_type=self.server.build_search_type(sch_type, project_code=proj_code)
                seq_sobject=self.server.get_by_code(search_type, sc_sobject["seq_code"])
                seq_code=seq_sobject['code']

                if "SEQ" in seq_code:
                    seq_name=seq_sobject['name']

        return {'sh_name':sh_name, 'sc_name':sc_name, 'seq_name':seq_name}

    def getShotSceneSequenceNames(self, tasks):
        results={}

        shSobjects=self.getParentSobjects(tasks)
        scSobjects=self.getParentSobjects(shSobjects, sch_type="%s/scn" % CUR_PROJECT, sch_code="scn_code")
        seqSobjects=self.getParentSobjects(scSobjects, sch_type="%s/seq" % CUR_PROJECT, sch_code="seq_code")

        sh_name=""
        sc_name=""
        seq_name=""

        for i in range(len(tasks)):
            if len(shSobjects) > 0:
                try:
                    sh_name=shSobjects[i]["name"]
                except: pass
                try:
                    sc_name=scSobjects[i]["name"]
                except: pass
                try:
                    seq_name=seqSobjects[i]["name"]
                except: pass

                results[tasks[i]["code"]]={'sh_name':sh_name, 'sc_name':sc_name, 'seq_name':seq_name}


        return results


    def getParentSobjects(self, sobjects, sch_type=None, sch_code=None, proj_code=CUR_PROJECT):
        sKeys=[]
        pSobjects=[]
        try:
            for sobj in sobjects:
                try:
                    skip=False
                    search_type=None
                    search_code=None

                    if not sch_type:
                        search_type=sobj["search_type"]
                    elif sch_type:
                        search_type=self.server.build_search_type(sch_type, project_code=proj_code)
                    if not sch_code:
                        search_code=sobj["search_code"]
                    else:
                        search_code=sobj[sch_code]

                    sk=self.server.build_search_key(search_type, search_code)
                    sKeys.append(sk)
                except Exception as msg:
                    print "foo 1"
                    search_code=sobj["search_code"]
                    print msg

            print sKeys
            if len(sKeys) > 0:
                pSobjects=self.server.get_by_search_key(sKeys)
        except Exception as msg:
            print "foo 2"
            print msg


        return pSobjects


    def addForceReplaceFileToSnapshot(self, snapshot_code, filepath, ftype="type", mode='upload', dirNaming=".", icon=True, directory=False, context="", replace=False, file_naming=None):
        isdone=False
        snapshot=None

        print "addForceReplaceFileToSnapshot..."

        i=0
        while isdone == False:
            if i > 20:
                return None
            try:

                basename=os.path.basename(filepath)
                base, ext=os.path.splitext(basename)
                cname=context
                ctokens = context.split("/")
                if len(ctokens) > 1:
                    cname = ctokens[1]

                if not file_naming:
                    file_naming="%s_%s_v{version}.{ext}" % (base, cname)

                if icon == True:
                    #file_naming="%s_icon_%s_v{version}.{ext}" % (base, context)
                    print  "1. dir Naming: ", dirNaming
                    print  "filepath: ", filepath

                    self.iconPath=filepath
                    self.iconDirnaming=dirNaming
                    snapshot=self.server.add_file(snapshot_code, filepath, mode=mode, dir_naming=dirNaming, create_icon=icon)
                elif directory:
                    print  "2. dir Naming: ", dirNaming
                    print  "filepath: ", filepath

                    file_naming="%s_v{version}" % basename
                    snapshot=self.server.add_directory(snapshot_code, filepath, file_type=ftype, mode=mode, dir_naming=dirNaming, file_naming="%s_v{version}" % basename)
                else:
                    print  "3. file Naming: ", file_naming
                    print  "dir Naming: ", dirNaming
                    print  "filepath: ", filepath

                    snapshot=self.server.add_file(snapshot_code, filepath, file_type=ftype, mode=mode, dir_naming=dirNaming, file_naming=file_naming)

                isdone=True
            except Exception as msg:
                print "Exception in addForceReplaceFileToSnapshot ...", msg

                fileExist=False
                sp_create=False
                if not icon:
                    print "no icon: ", msg

                try:
                    print "sattr addForceReplaceFileToSnapshot", str(msg)

                    sttr=str(msg)
                    st=sttr.index('[')+1
                    ed=sttr.index(']')
                    filen=sttr[st:ed]
                    ftokens=self.getTonkenizedPath(filen)
                    remfile=filen

                    fftokens=remfile.split(":")
                    if len(fftokens) > 1:
                        remfile=("%s/%s" % (serverPath, fftokens[1]))

                    fileExist=True

                    if "does not exist" in str(msg):
                        if mode != "upload":
                            try:
                                handoff_dir=os.path.dirname(remfile)

                                fileBasname=os.path.basename(filepath)
                                handof_fpath='%s/%s' % (handoff_dir, fileBasname)
                                print "Recopy %s to %s" % (filepath, handoff_dir)
                                print "1. handoff_path %s" % (handof_fpath)
                                if not os.path.exists(handof_fpath):
                                    print "2. handoff_path %s" % (handof_fpath)
                                    os.makedirs(handoff_dir)
                                if directory:
                                    print "3. filepath %s, handof_fpath %s" % (filepath, handof_fpath)
                                    shutil.copytree('%s' % filepath, '%s' % handof_fpath)
                                else:
                                    print "4. filepath %s, handof_fpath %s" % (filepath, handof_fpath)
                                    shutil.copyfile('%s' % filepath, '%s' % handof_fpath)
                                while os.path.exists(handof_fpath) and not os.access(handof_fpath, os.R_OK):
                                    pass
                            except Exception as msg:
                                print "5. error %s" % (msg)
                                print "ERROR", msg
                                return None

                    elif directory:
                        kwargs={'dir':'%s' % remfile}
                        remResult=self.server.execute_python_script('dom/deleteDirectory', kwargs)
                        #print "delete", remfile
                    else:
                        print "delete", remfile
                        if replace:
                            kwargs={'filename':'%s' % remfile}
                            remResult=self.server.execute_python_script('dom/deleteFile', kwargs)


                except Exception as msg:
                    print "ERROR", msg
                    return None
            i += 1

        return snapshot

    def createAssetTaskSnapShot(self, tacticSOBJECT, pixmap=None, savePath=None, basename=None, desc="", isCurrent=True, isParent=False, serverPath="", category="asset", tag=None, version=None):
        '''
            Creat the task snapshot to add files to

            tacticSOBJECT - the SObject to extract the search_key and context
            pixmap - pixmap file to set thumble
            savePath - Temp directory to save a file
            basename - The basename of the file
            desc - description of snapshot
            isCurrent - if current is true snapshot will be set as current version
            return - list of snapshot sobject and snapshot_code
        '''
        #print tacticSOBJECT
        search_key = tacticSOBJECT['__search_key__']
        context = ""
        try:
            context = tacticSOBJECT['context'].split('/')[0]
        except:
            context = "icon"
            pass

        scontext = context
        if tag is not None and context != "icon":
            scontext = "%s_%s" % (context, tag)

        print tacticSOBJECT


        snapshot = self.server.create_snapshot(search_key, scontext, description=desc, is_current=isCurrent, triggers=False)
        print "HERE HI", snapshot
        snapshot_code = snapshot['code']
        if version:
            self.updateSnapshotVersionFromFile(snapshot, version)

        if basename is not None:
            iconpath=("%s/%s.jpg" % (savePath, basename))
        elif savePath is not None:
            iconpath=("%s/icon.jpg" % savePath)

        if pixmap is not None:
            #print "ICON PATH", iconpath
            if pixmap.save(iconpath, "JPEG"):
                dirNaming = ""
                basename=os.path.basename(iconpath)
                handoff_dir = self.server.get_handoff_dir()
                shutil.copyfile('%s' % iconpath, '%s/%s' % (handoff_dir, basename))

                if isParent == True:
                    dirNaming = '{project.code}/%s/{name}_{code}/icons' % category
                else:

                    if "sequences" in category:
                        shInfo=self.getShotSceneSequenceName(tacticSOBJECT)
                        category="sequences/%s/%s" % (shInfo["seq_name"], shInfo["sc_name"])

                    #print "CAT", category
                    dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/icons/{context[1]}' % (category, context)

                sp=self.addForceReplaceFileToSnapshot(snapshot_code, iconpath, mode='copy', dirNaming=dirNaming, icon=True, replace=True)

                os.remove(iconpath)

        print "HERERERE", [snapshot, snapshot_code]
        return [snapshot, snapshot_code]


    def addFileToSnapshot(self, snapshot_code, file, type='any', mode="upload", sobject=None, category="asset", isImage=False, isPlayblast=False, directory=False, group=False, groupFileRange="", isMaps=True, tag=None, replace=False, file_naming=None, yeti=False, shave=False):
        '''
            Add File to snapshot and directory name convention speficied by type

            snapshot_code - the snapshot_code to add a file
            file - the file path to add
            type - basename of the file
            mode - copy/upload/inplace
            sobject - the SObject to extrat the directory name convention (maps folder is created in director as model)
        '''
        dirNaming = ''
        context = sobject['context'].split('/')[0]

        if "sequences" in category:
            shInfo=self.getShotSceneSequenceName(sobject)
            category="sequences/%s/%s" % (shInfo["seq_name"], shInfo["sc_name"])

        tokens = self.getTonkenizedPath(file)
        if tokens[2] in (".ma", ".mb", ".obj", ".hip") and tag in ("Sim",):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/simulation/scenes/{context[1]}' % category
        elif tokens[2] in (".ma", ".mb", ".obj", ".hip"):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/scenes/{context[1]}' % (category, context)
        elif tokens[2] ==".nk":
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/{context[1]}' % (category, context)
        elif tokens[2] in (".xml", ".mcx"):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/scenes/cache/{context[1]}' % (category, context)
        elif tokens[2] == ".vdb":
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/openVDB/{context[1]}' % (category, context)
        elif tokens[2] in (".abc",):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/alembic/{context[1]}' % (category, context)
        elif tokens[2] in (".flw",):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/realFlow/{context[1]}' % (category, context)
        elif tokens[2] in (".txt",):
            dirNaming = '{project.code}/%s' % category
        elif tokens[2] in (".tif", ".jpg", ".png", ".bmp", ".tga", ".tx", ".exr", ".iff", ".hdr") and not isImage:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/maps/{context[1]}' % (category, context)
        elif tokens[2] in (".tif", ".jpg", ".png", ".bmp", ".tga", ".tx", ".exr", ".iff", ".hdr") and isImage:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/images/{context[1]}' % (category, context)
        elif tokens[2] == ".mov" and not isPlayblast:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/video/{context[1]}' % (category, context)
        elif tokens[2] == ".mov" and isPlayblast:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/playblast/{context[1]}' % (category, context)
        elif tokens[2] in (".wav", ".mp3"):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/audio/{context[1]}' % (category, context)
        elif tokens[2] == ".psd":
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/photoshop/{context[1]}' % (category, context)
        elif tokens[2] in (".ztl", ".ZTL"):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/zbrush/{context[1]}' % (category, context)
        elif tokens[2] in (".mra",):
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/mari/{context[1]}' % (category, context)
        elif directory and yeti:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/yeti' % (category, context)
        elif directory and shave:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/shave' % (category, context)
        elif directory and not isMaps:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/scenes' % (category, context)
        elif directory and isMaps:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/maps' % (category, context)
            if tag:
                dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/maps' % (category, context)
        else:
            dirNaming = '{project.code}/%s/{parent.name}_{parent.code}/{process[0]}/%s/others/{context[1]}' % (category, context)

        print "ADDED FILE ", file, ", dir ", dirNaming

        sp=None
        if group:
            sp=self.server.add_group(snapshot_code, file, file_type=type, file_range=groupFileRange, mode=mode)
        elif directory:
            #sp=self.server.add_directory(snapshot_code, file, file_type=type, mode=mode, dir_naming=dirNaming)
            sp=self.addForceReplaceFileToSnapshot(snapshot_code, file, ftype=type, mode=mode, dirNaming=dirNaming, icon=False, directory=True)
        else:
            #print "ADD FILE", file
            sp=self.addForceReplaceFileToSnapshot(snapshot_code, file, ftype=type, mode=mode, dirNaming=dirNaming, icon=False, context=context, replace=replace, file_naming=file_naming)

        #snapshot = self.server.add_file(snapshot_code, file, file_type=type, mode=mode, dir_naming=dirNaming)
        #self.server.clear_upload_dir()

        #print "ADDED FILE", file
        return sp


    def removeSnapshotSObject(self, tacticSOBJECT):
        search_key = tacticSOBJECT['__search_key__']
        sobject=self.server.retire_sobject(search_key)

    def deleteSObject(self, tacticSOBJECT):
        search_key = tacticSOBJECT['__search_key__']
        self.server.delete_sobject(search_key)

    def deleteSnapshot(self, serverPath, snapshot_code):
        '''
            Delete the snapshot and all files added to it

            serverPath - the server path to replace
            snapshot_code - the snapshot code
        '''
        # get all of the file paths
        snapshot = self.getSnapshotSObjectByCode(snapshot_code)
        file_paths = self.getAllPathFromSnapshot(snapshot_code)
        files = self.getAllFileSObjectFromSnapshot(snapshot_code)
        for file in files:
            search_key = file.get('__search_key__')
            self.server.delete_sobject(search_key)

        # remove the files from the repo
        for file_path in file_paths:
            tokens = self.getTonkenizedPath(file_path)
            ttokens=[]
            ttokens=tokens[0].split(":")

            #print tokens, ttokens
            if len(ttokens) == 1:
                filename = ("%s/%s%s" % (tokens[0], tokens[1], tokens[2]))
                #print filename
            else:
                filename = ("%s/%s/%s%s" % (serverPath, ttokens[1], tokens[1], tokens[2]))
                #print filename
            try:
                os.remove(filename)
            except: pass

        if len(snapshot) > 0:
            search_key = snapshot[0].get('__search_key__')
            self.server.delete_sobject(search_key)

    def getLatestSnapshotVersion(self, tacticSOBJECT, tag=None):
        snapshot_version=None
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context'].split('/')[0]
            process = tacticSOBJECT['process']
            code = tacticSOBJECT['code']
            project_code = tacticSOBJECT['project_code']

            filters = []
            filters.append(("project_code", project_code))
            filters.append(("search_code", code))

            if tag:
                context="%s_%s" % (context, tag)

            filters.append(("process", context))

            filters.append(("context", context))
            filters.append(("is_latest", True))

            #print filters

            result=self.server.query_snapshots(filters=filters)
            #print "LAST SP", result
            snapshot_version = result[0]['version']
        except Exception as msg:
            #print msg
            pass
        return snapshot_version



    def getCurrentSnapshots(self, tacticSOBJECT, isCurrent=True):
        snapshots={}
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context'].split('/')[0]
            process = tacticSOBJECT['process']
            code = tacticSOBJECT['code']
            project_code = tacticSOBJECT['project_code']

            filters = []
            order_bys = ['timestamp']
            filters.append(("project_code", project_code))
            filters.append(("search_code", code))
            #filters.append(("process", context))
            #filters.append(("context", context))
            filters.append(("is_current", isCurrent))

            #print filters

            snapshots=self.server.query_snapshots(filters=filters, order_bys=order_bys, include_paths_dict=True)
        except Exception as msg:
            #print msg
            pass
        return snapshots


    def getPathDictFromCurrentSnapshots(self, tacticSOBJECT, sub_types=[]):
        paths={}
        snapshots=self.getCurrentSnapshots(tacticSOBJECT)

        for sp in snapshots:
            path_dict=sp['__paths_dict__']
            for key in path_dict.keys():
                idx=key.rfind('_')
                if idx != -1:
                    if key[idx:] in sub_types and path_dict[key][0] not in paths:
                        paths[key]=path_dict[key][0]
                    elif len(sub_types) == 0:
                        paths[key]=path_dict[key][0]

        return paths


    def getSnapshotByCode(self, code):
        snapshot=[]
        try:
            filters = []
            filters.append(("project_code", self.project))
            filters.append(("code", code))

            snapshot=self.server.query_snapshots(filters=filters, include_paths_dict=True)
        except Exception as msg:
            pass
        return snapshot


    def updateSnapshotsContextWithStrInFiletype(self, snapshot, substr, sub_types=[]):
        result={}
        count=0
        data={}
        lastKey=""
        try:
            path_dict=snapshot['__paths_dict__']
            for key in path_dict.keys():
                idx=key.rfind('_')
                if idx != -1:
                    if key[idx:] in sub_types:
                        count += 1
                        if substr in key:
                            lastKey=key

            if count == 1 and lastKey != "":
                #print "updating", lastKey, snapshot['context']
                context=snapshot['context']
                #idx=context.rfind('_')
                #if idx != -1:
                #   print context[:idx]

                if count == 1 and substr not in context:
                    data['context']="%s_%s" % (context, substr)
                    #data['context']=context[:idx]

                    data['is_current']=True
                    data['is_latest']=True
                    result=self.server.update(snapshot['__search_key__'], data=data)
        except Exception as msg:
            print msg
            pass

        return result


    def getLastestFilepathsFromSObject(self, tacticSOBJECT, type="", fileName="", sub_types=[]):
        types=[]
        file_paths=[]
        fileSobjs=[]
        try:
            project_code = tacticSOBJECT['project_code']
            code = tacticSOBJECT['code']

            order_bys = ['file_name']
            filters = []
            filters.append(("project_code", project_code))
            filters.append(("search_code", code))

            if type != "":
                filters.append(("type", type))

            if fileName != "":
                filters.append(("file_name", fileName))

            result=self.server.query("sthpw/file", filters=filters, order_bys=order_bys)

            c=len(result)
            for i in range(c):
                type=result[c-i-1]['type']
                idx=type.rfind('_')
                if idx != -1:
                    if type[idx:] == "_ma":
                        styp="%s_mb" % type[:idx]
                        types += [styp]
                    if type[idx:] == "_mb":
                        styp="%s_ma" % type[:idx]
                        types += [styp]

                if type not in types:
                    if len(sub_types) > 0:
                        for sb_type in sub_types:
                            if sb_type in type[-4:]:
                                types += [type]
                                path="%s%s" % (result[c-i-1]['checkin_dir'], result[c-i-1]['file_name'])
                                file_paths += [path]
                                fileSobjs.append(result[c-i-1])
                    else:
                        types += [type]
                        path="%s%s" % (result[c-i-1]['checkin_dir'], result[c-i-1]['file_name'])
                        file_paths += [path]
                        fileSobjs.append(result[c-i-1])
                types += [type]

        except Exception as msg:
            print msg
            pass
        return file_paths, fileSobjs



    def getUserTasksAssigned(self, username=""):
        #print "calling getUserTasksAssigned"
        #currtime= time.time()
        tasks=[]
        if username != "":
            self.username=username
        try:
            assigned = self.username
            project_code = self.project

            filters = []
            filters.append(("project_code", project_code))
            filters.append(("assigned", assigned))
            #filters.append(("supervisor", assigned))
            filters.append(("status", ("In Progress", "Assigned", "Review", "Waiting")))
            tasks=self.server.query("sthpw/task", filters=filters)
            '''
            filters = []
            filters.append(("project_code", project_code))
            filters.append(("supervisor", assigned))
            filters.append(("status", ("In Progress", "Assigned", "Review")))
            subtasks=self.server.query("sthpw/task", filters=filters)

            for task in subtasks:
                if task not in tasks:
                    tasks.append(task)
            '''

            #for task in tasks:
            #   print task["status"]

            #pprint(tasks)
        except Exception as msg:
            print msg
            pass

        #elapsed=time.time() - currtime
        #print "elapsed time %s" % elapsed
        return tasks

    def getSupervisorTasksAssigned(self):
        #print "calling getUserTasksAssigned"
        #currtime= time.time()
        tasks=[]
        try:
            assigned = self.username
            project_code = self.project

            filters = []
            filters.append(("project_code", project_code))
            filters.append(("supervisor", assigned))
            filters.append(("status", ("In Progress", "Assigned", "Review")))
            subtasks=self.server.query("sthpw/task", filters=filters)

            for task in subtasks:
                if task not in tasks:
                    tasks.append(task)

        except Exception as msg:
            print msg
            pass

        return tasks


    def getScenesFromSeqSObject(self, tacticSOBJECT):
        result=[]
        try:
            code = tacticSOBJECT['code']
            project_code = tacticSOBJECT['project_code']

            filters = []
            #filters.append(("project_code", project_code))
            filters.append(("search_code", code))

            result=self.server.query("%s/scn" % CUR_PROJECT, filters=filters)

        except Exception as msg:
            #print msg
            pass
        return result

    def getSeqSObjectbyName(self, seq_name):
        result=[]
        try:
            filters = []
            #filters.append(("project_code", project_code))
            filters.append(("name", seq_name))
            result=self.server.query("%s/seq" % CUR_PROJECT, filters=filters)


        except Exception as msg:
            #print msg
            pass
        return result

    def getScnSObjectbyNameAndSeqCode(self, scn_name, seq_code):
        result=[]
        try:
            filters = []
            #filters.append(("project_code", project_code))
            filters.append(("name", scn_name))
            filters.append(("seq_code", seq_code))
            result=self.server.query("%s/scn" % CUR_PROJECT, filters=filters)

        except Exception as msg:
            #print msg
            pass
        return result

    def getShtSObjectbyName(self, seq_code, scn_code):
        result=[]
        try:
            filters = []
            filters.append(("seq_code", seq_code))
            filters.append(("scn_code", scn_code))
            result=self.server.query("%s/shot" % ALIAS_PROJECT, filters=filters)

        except Exception as msg:
            #print msg
            pass
        return result

    def getSceneSObjectsBySeqCode(self, seq_code):
        result=[]
        try:
            filters = []
            filters.append(("seq_code", seq_code))
            result=self.server.query("%s/scn" % CUR_PROJECT, filters=filters)

        except Exception as msg:
            #print msg
            pass
        return result

    def getTasksFromSObjectSameProcess(self, tacticSOBJECT):
        result=[]
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context']
            process = tacticSOBJECT['process']
            code = tacticSOBJECT['code']
            project_code = tacticSOBJECT['project_code']

            filters = []
            filters.append(("project_code", project_code))
            filters.append(("search_code", code))
            filters.append(("process", process))

            #print filters

            result=self.server.query(filters=filters)

        except Exception as msg:
            #print msg
            pass
        return result

    def getTaskSObjectMultiAssigned(self, Sobject):
        tsobject=Sobject
        sobjects, assignedUsers=self.getTaskAssignedUsers(Sobject['search_code'], Sobject['process'], Sobject['context'], order_bys=["timestamp"])
        #print "MULTI", sobjects
        if len(sobjects) > 1:
            #print "MULTI", sobjects
            #return sobjects[0]

            for sobj in sobjects:
                self.curMetadata=self.getMetadataFromSnapshot(sobj)
                try:
                    self.curMetadata['Basename']
                    tsobject=sobj
                    break
                except: pass
            if len(tsobject.keys()) == 0:
                return Sobject

        else:
            return Sobject
        return tsobject


    def checkSObjectInList(self, sobject, ListSobject):
        isIn=False
        #print sobject
        for sobj in ListSobject:
            try:
                #print sobject['code'], sobj['code']
                if sobject['code'] == sobj['code']:
                    isIn=True

                    break
            except: pass
        return isIn

    def getAllSnapshots(self, tacticSOBJECT, tag=None):
        result=None
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context']
            process = tacticSOBJECT['process']
            code = tacticSOBJECT['code']
            project_code = tacticSOBJECT['project_code']

            order_bys = ['version']
            #order_bys = ['timestamp']
            filters = []
            filters.append(("project_code", project_code))
            filters.append(("search_code", code))
            if tag:
                context="%s_%s" % (context, tag)
            filters.append(("process", context))
            filters.append(("context", context))

            #print filters

            result=self.server.query_snapshots(filters=filters, order_bys=order_bys, include_paths_dict=True)
        except Exception as msg:
            #print msg
            pass
        return result


    def getSnapshotCodeFromSOBJECT(self, tacticSOBJECT):
        '''
            Get snapshot from given SObject
            tacticSOBJECT - the SObject to extract the search_key and context
            return the snapshot code associated
        '''
        snapshot_code=None
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context']
            #print context
            snapshot = self.server.get_snapshot(search_key, context, version=0)
            if len(snapshot.keys()) == 0:
                snapshot = self.server.get_snapshot(search_key, context)
            #print snapshot
            snapshot_code=snapshot.get('code')
        except: pass
        return snapshot_code


    def getSnapshotVersionFromSOBJECT(self, tacticSOBJECT):
        '''
            Get snapshot from given SObject
            tacticSOBJECT - the SObject to extract the search_key and context
            return the snapshot code associated
        '''
        snapshot_version=None
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context']
            snapshot = self.server.get_snapshot(search_key, context, version=0)
            snapshot_version=snapshot.get('version')

        except: pass
        return snapshot_version

    def getMetadataFromSnapshot(self, tacticSOBJECT, tag=None):
        '''
            Get metada SObject from given SObject
            tacticSOBJECT - the SObject to extract the search_key and context
            return a SOBject metadata
        '''
        metadata={}
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context'].split('/')[0]
            if tag:
                context="%s_%s" % (context, tag)
            snapshot = self.server.get_snapshot(search_key, context, version=0)
            if len(snapshot.keys()) == 0:
                snapshot = self.server.get_snapshot(search_key, context)
            metadata = snapshot['metadata']
            #print snapshot
        except: pass

        return metadata

    def getSObjectSnapshotWithMetadata(self, tacticSOBJECT, tag=None):
        '''
        Get Snapshot SObject from given SObject
        tacticSOBJECT - the SObject to extract the search_key and context
        return a SOBject snapshot
        '''
        snapshot = {}
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = tacticSOBJECT['context'].split('/')[0]
            if tag:
                context="%s_%s" % (context, tag)
            snapshot = self.server.get_snapshot(search_key, context, version=0)
            if len(snapshot.keys()) == 0:
                snapshot = self.server.get_snapshot(search_key, context)

        except: pass

        return snapshot



    def inplaceChekin(self, snapshot_code, sobject, paths=[]):
        '''
            Check a file without copy/upload/move to Tactic directory
            The inplaceChekin function is require to link the file again to snapshot when renamed

            snapshot_code - the snapshot_code to add a file
            sobject - the SObject to extract the context
        '''

        #print "PATHS", paths
        for path in paths:
            tokens = self.getTonkenizedPath(path)
            #print "HERE END"
            type = tokens[2][1:]
            key = self.removeTagContext(tokens[1], sobject['context'])
            self.addFileToSnapshot(snapshot_code, path, '%s_%s' % (key, type), sobject=sobject, mode="inplace")


    def inplaceChekinDirectory(self, snapshot_code, dir=""):
        '''
            Check a file without copy/upload/move to Tactic directory
            The inplaceChekin function is require to link the file again to snapshot when renamed

            snapshot_code - the snapshot_code to add a file
            sobject - the SObject to extract the context
        '''
        if dir != "":
            basename = os.path.basename(dir)
            dirname = os.path.dirname(dir)
            ftype = "%s_dir" % basename
            self.server.add_directory(snapshot_code, dir, file_type=ftype, mode="inplace", dir_naming=dirname, file_naming=basename)

    def assetSimpleCheckin(self, tacticSOBJECT, file, type='any', desc="", snapshot_code=None):
        snapshot=None
        try:
            search_key = tacticSOBJECT['__search_key__']
            context = ""
            try:
                context = tacticSOBJECT['context']
            except:
                context = "icon"

            snapshot = self.server.simple_checkin(search_key, context, file, file_type=type, description=desc, mode="upload")
            self.server.clear_upload_dir()
        except: pass
        return snapshot

    '''
    def getSnapShotByCode(self, snapshot_code):
        search_key = tacticSOBJECT['__search_key__']
        context = tacticSOBJECT['context']
        snapshot = self.server.get_snapshot(search_key, context, include_paths_dict=True)
        return snapshot
    '''

    def getBasePaths(self):
        paths=self.server.get_base_dirs()
        return paths

    def getPathsFromSObject(self, tacticSOBJECT):
        '''
            Get paths from given SObject
            tacticSOBJECT - the sobject to extract search_key and context
            return list of paths
        '''
        search_key = tacticSOBJECT['__search_key__']
        context = tacticSOBJECT['context'].split('/')[0]
        paths=self.server.get_paths(search_key, context)
        return paths

    def getSnapShotFromSOBJECT(self, tacticSOBJECT, paths=True, tag=None):
        '''
            Get Snapshot from given SObject
            tacticSOBJECT - the SObject to extract search_key and context
            paths - if True return snapshot including paths
            return snapshot SObject (dictionary)
        '''
        search_key = tacticSOBJECT['__search_key__']
        context = tacticSOBJECT['context'].split('/')[0]
        if tag:
            context="%s_%s" % (context, tag)
        snapshot = self.server.get_snapshot(search_key, context, include_paths_dict=paths, version=0)

        if len(snapshot.keys()) == 0:
            snapshot = self.server.get_snapshot(search_key, context, include_paths_dict=paths)

        return snapshot

    #def getAllPathFromSnapshot(self, snapshot_code, types=['maya', 'proxy']):
    def getAllPathFromSnapshot(self, snapshot_code):
        '''
            Get All path from snaphot by given snapshot_code
            snapshot_code - the snapshot_code to look at
            return list of basename of all files checked in
        '''
        fpaths=[]
        try:
            paths=self.server.get_all_paths_from_snapshot(snapshot_code, expand_paths=True)
            #paths=self.server.get_all_paths_from_snapshot(snapshot_code, expand_paths=True, file_types=types)
            for ppath in paths:
                #basename=os.path.basename(ppath)
                dirname=os.path.dirname(ppath)
                if "/icon" not in dirname or "/icons" not in dirname:
                    fpaths.append(ppath)
        except: pass
        return fpaths

    def getAllPathFromSOBJECT(self, tacticSOBJECT):
        sp_code=self.getSnapshotCodeFromSOBJECT(tacticSOBJECT)
        paths=self.getAllPathFromSnapshot(sp_code)
        return paths

    def getIconPathFromSnapshot(self, snapshot_code):
        '''
            Get All path from snaphot by given snapshot_code
            snapshot_code - the snapshot_code to look at
            return list of basename of all files checked in
        '''
        fpaths=[]
        try:
            #paths=self.server.get_all_paths_from_snapshot(snapshot_code, expand_paths=True)
            ipath=self.server.get_path_from_snapshot(snapshot_code)
            if ipath:
                print "ICON PATH", ipath
                fpaths.append(ipath)
            '''
            #paths=self.server.get_all_paths_from_snapshot(snapshot_code, expand_paths=True, file_types=types)
            snapshots=self.getCurrentSnapshots(tacticSOBJECT)
            for ppath in paths:
                basename=os.path.basename(ppath)
                dirname=os.path.dirname(ppath)
                if "/icon" in dirname or "/icons" in dirname:
                    if "_icon" not in basename and "_web" in basename:
                        fpaths.append(ppath)
                        break
            '''
        except: pass
        return fpaths

    def getFileTagVersionFromSObject(self, tacticSOBJECT, file_type, tag=None):
        version=-1
        snapshots=self.userQuery.getAllSnapshots(tacticSOBJECT)
        try:
            paths=snapshots[-1]['__paths_dict__']

            stp=False
            for key in paths.keys():
                if key not in ("icon", "web", "main", "mapsDir"):
                    for path in paths[key]:
                        basename=os.path.basename(path)
                        if file_type in basename:
                            version=self.userQuery.getTagVersion(basename)
                            print version

        except Exception as msg:
            print "HERE", msg
            pass

        return version

    def getIconPathFromSObject(self, tacticSOBJECT):
        '''
            Get All path from snaphot by given snapshot_code
            snapshot_code - the snapshot_code to look at
            return list of basename of all files checked in
        '''
        ipaths=[]

        snapshots=self.getCurrentSnapshots(tacticSOBJECT)
        for sp in snapshots:
            try:
                path_dict=sp["__paths_dict__"]
                if "icon" in path_dict.keys():
                    ipaths.extend(path_dict["icon"])
                    #print ipaths
                    break
            except Exception as msg:
                #print msg
                pass
        return ipaths

    def getServerPaths(self, tacticSOBJECT):
        '''
            Get server paths by given SObject
            tacticSOBJECT - the sobject to extract search_key and context
            return list of paths
        '''
        search_key = tacticSOBJECT['__search_key__']
        context = tacticSOBJECT['context']

        paths=self.server.get_paths(search_key, context, versionless=False)
        return paths

    def getAllBasenameFromSnapshot(self, snapshot_code):
        '''
            Get All file basename from snaphot
            snapshot_code - the snapshot_code to look at
            return list of basename of all files checked in
        '''
        basenames=[]
        paths=self.getAllPathFromSnapshot(snapshot_code)
        for path in paths:
            basenames.append(os.path.basename(path))
        return basenames

    def getFileVersionCount(self, dir, basename, ext):
        '''
            Get number of file on given directory with given basename and extension

            dir - the directory to check the file
            basename - the basename of the file to rename
            ext - the extension of file to rename
            return the file count
        '''
        v=0
        basename=self.removeTagVersion(basename)
        files=glob.glob("%s/%s*.%s" % (dir, basename, ext))
        try:
            tokens=self.getTonkenizedPath(files[0])
            basename=self.removeTagVersion(tokens[1])

            v=len(files)
        except Exception as msg:
            print msg
        return v

    def renameFileVersion(self, dir="", basename="", ext=""):
        '''
            Rename file with correct tag version on the given dir
            This is requery to fix the multifile checkin in different time. Tactic create version file accroding to snapshot version

            dir - the directory to check the file
            basename - the basename of the file to rename
            ext - the extension of file to rename
            return renamed file with correct tag version
        '''
        newname=""
        try:
            #basename=self.removeTagVersion(basename)
            files=glob.glob("%s/%s*.%s" % (dir, basename, ext))
            newname=files[0]
            '''tokens=self.getTonkenizedPath(files[0])
            basename=self.removeTagVersion(tokens[1])
            v=len(files)
            newname=("%s/%s_v%03d.%s" % (dir, basename, v, ext))
            newname=files[0]
            if newname!=files[-1]:
                return newname
                #os.renames(files[-1], newname)
            else:
                newname=""'''
        except Exception as msg:
            print msg
        return newname

    def updateSObjectData(self, search_key, data):
        result = self.server.update(search_key, data)
        return result

    def getTonkenizedPath(self, path):
        '''
            Tokenize string path into tokens
            path - the path string
            return list of tokens
        '''
        directory=os.path.dirname(path)
        basename=os.path.basename(path)
        basenameNoExt, extension=os.path.splitext(basename)
        return [directory, basenameNoExt, extension]

    def removeTagVersion(self, name):
        '''
            Find and Remove version Tag on name
            name - the source string
            return string name without version tag
        '''
        basename=name
        padding=re.findall(r'(\d+)', name)
        count=len(padding)

        if count > 0:

            padding=padding[count-1]
            version=('v%s' % padding)
            basename=self.removeTagContext(name, version)
            #print "BASESS", name, basename, padding
        return basename

    def getTagVersion(self, name, integer=True):
        '''
            Find and Remove version Tag on name
            name - the source string
            return string name without version tag
        '''
        version=-1
        padding=re.findall(r'(v\d+)', name)
        count=len(padding)

        if count > 0:
            if integer:
                padding=padding[count-1][1:]
                version=int(padding)
            else:
                padding=padding[count-1]
                version=padding

        return version

    def removeTagVersion2(self, name):
        basename=name
        padding=re.findall(r'(v\d+)', name)
        count=len(padding)

        index=-1
        n=0
        version=""
        for pad in padding:
            try:
                version=('%s' % pad)
                index=name.rindex(version)
            except: pass
            if index != -1:
                c=index - 1
                n=len(version)
                if name[c] != '_':
                    basename=name[:index]
                else:
                    basename=name[:c]
                break


        c=index + len(version)
        if index > -1 and (c - 1) < len(name):
            basename += name[c:]

        #basename=re.sub(re.escape("_%s" % version), '', basename)
        return basename

    def removeTagContext(self, s, context):
        '''
            Remove context name from string
            s - the soruce string
            context - the substring context to be removed from source
            return the split string without context
        '''
        index=-1
        try:
            index=s.rindex(context)
        except: pass

        if index > 5:
            index -= 1
            return s[:index]
        else:
            return s

    def removeUntilContext(self, s, context):
        '''
            Remove context name from string
            s - the soruce string
            context - the substring context to be removed from source
            return the split string without context
        '''
        index=-1
        try:
            index=s.rindex(context)
        except: pass

        if index > 1:
            index += len(context)
            return s[index:]
        else:
            return s

    def findStringInBetween(self, s, first, last ):
        '''
            Find string in between by given strings
            s - the source string
            first - the first substring to find
            last - the second substring t find
        '''
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def replaceStringInBetween(self, s, first, last, strReplace):
        '''
            Replace string in between by given string
            s - the source string
            first - the first substring to find
            last - the second substring t find
            strReplace - the replacement string
        '''
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            strlist=[]
            strlist.append(s[:start])
            strlist.append(strReplace[:])
            strlist.append(s[end:])
            s=''.join(strlist)
            return s
        except ValueError:
            return ""

    def getIncrementedVersionFilename(self, filename):
        newpath=""
        if os.path.exists(filename):
            tokens=self.getTonkenizedPath(filename)
            notagName=self.removeTagVersion(tokens[1])

            files=glob.glob("%s/%s*%s" % (tokens[0], notagName, tokens[2]))
            if len(files) == 0:
                return newpath

            files.sort()
            lastfile=files[-1]

            tokens1=self.getTonkenizedPath(lastfile)
            padding=re.findall(r'(\d+)', tokens1[1])

            if len(padding) > 0:
                padding=padding[-1]
                value=int(padding)
                version="v%03d" % (value + 1)

                newpath="%s/%s_%s%s" % (tokens[0], notagName, version, tokens[2])

        return newpath

    def getIncrementedVersionFolder(self, dirname):
        newpath=""
        if os.path.exists(dirname):
            tokens=self.getTonkenizedPath(dirname)
            notagName=tokens[1]

            ntokens=re.split("_v", notagName)
            if len(ntokens) > 1:
                notagName=ntokens[0]

            print notagName
            files=[dir for dir in os.listdir(tokens[0]) if os.path.isdir(os.path.join(tokens[0], dir)) and ('%s_v' % notagName) in dir]
            if len(files) == 0:
                return newpath

            files.sort()
            lastfile=files[-1]

            tokens1=self.getTonkenizedPath(lastfile)
            padding=re.findall(r'(\d+)', tokens1[1])

            if len(padding) > 0:
                padding=padding[-1]
                value=int(padding)
                version="v%03d" % (value + 1)

                newpath="%s/%s_%s" % (tokens[0], notagName, version)

        return newpath

    def checkOutAsset(self, tacticSOBJECT, checkoutFilename, serverDir="", spversion=-1, fileTypes=[], toDir=""):
        '''
            tacticSOBJECT - Tactic Sobject
            checkoutFilename - basename of the file to checkout
            serverDir - the server path to checkout
            spversion - version of snapshot
            fileTypes - type of files to checkout
        '''
        search_key = tacticSOBJECT['__search_key__']
        context = tacticSOBJECT['context']
        allFiles=[]
        toSandbox=False
        if len(toDir)== 0:
            toSandbox=True
        for type in fileTypes:
            files=self.server.checkout(search_key, context, version=spversion, file_type=type, checkoutFilename=checkoutFilename, serverDir=serverDir, to_dir=toDir, to_sandbox_dir=toSandbox)
            allFiles.extend(files)
        return allFiles


    def getIconFromSObject(self, tacticSOBJECT):
        '''
            Get Icon file path from snapshot
            tacticSOBJECT - tactic SObject
        '''
        search_key = tacticSOBJECT['__search_key__']
        context = 'icon'
        snapshot = self.server.get_snapshot(search_key, context, version=0)

        if len(snapshot.keys()) == 0:
            snapshot = self.server.get_snapshot(search_key, context)

        snapshot_code = snapshot.get('code')
        paths = self.getAllPathFromSnapshot(snapshot_code)
        return paths

    def updateFileLockStatus(self, username, taskCode, status="unlocked"):
        try:
            SObject=self.getTaskByCode(taskCode)[0]
            localtime=time.asctime(time.localtime(time.time()))

            sp=self.getSObjectSnapshotWithMetadata(SObject)
            metadata=sp['metadata']
            print metadata

            metadata["lockInfo"]={'status':status, 'who':str(username), 'when':localtime}
            print "File lock info update:", metadata["lockInfo"]

            data={
                'metadata': metadata
            }

            up_sp=self.updateSObjectData(sp['__search_key__'], data)

        except Exception as msg:
            print msg
            pass
        return status


    def checkUpdateVersion(self, taskCode, version=""):
        task=self.getTaskByCode(taskCode)
        if len(task) > 0:
            snapshots=self.getCurrentSnapshots(task[0])

    def insertSearchType(self, search_type, data={}):
        result={}
        if search_type and len(data.keys()) > 0:
            result=self.server.insert(search_type, data, use_id=True)

        return result

    def createMultiTasks(self, search_key, data={}):
        tasks=[]
        for process in data.keys():
            contexts=data[process]
            for context in contexts:
                task=self.server.create_task(search_key, process=process, description="auto generated")
                tasks.append(task)
        return tasks

    def updateSnapshotVersionFromFile(self, snapshot, fversion=None):
        version=None
        if snapshot and fversion and fversion != "":
            uversion=int(fversion[1:])

            data={
                'version':uversion
            }
            self.updateSObjectData(snapshot["__search_key__"], data)
            version="v%03d" % uversion
        return version

    def checkAndUpdateSnapshotVersion(self, path):
        vversion=None
        vtokens=re.split('v\d{3}', path)
        #----------- CHECK FOR LAST VERSION AND UPDATE SNAPSHOT ----------------
        print vtokens
        if len(vtokens) > 1:
            allfiles=glob.glob("%sv???%s" % (vtokens[0], vtokens[1]))

            if len(allfiles) == 0:
                return vversion

            allfiles.sort()

            versions=re.findall("v\d{3}", allfiles[-1])
            #print "VERSION", versions
            if len(versions) > 0:
                #ssnapshot=self.getSnapshotByCode(snapshot_code)
                vupdate=int(versions[-1][1:])+1
                vversion="v%03d" % vupdate
                #vversion=self.updateSnapshotVersionFromFile(ssnapshot[0], "v%s" % vupdate)
                #print "UPDATING SNAPSHOT to %s" % vversion
        return vversion













