#!/usr/bin/python


import xml.etree.ElementTree as ET
import shutil
import sys
import glob
import os

sourcedir = sys.argv[1]
targetdir = sys.argv[2]
print "source dir: ", sourcedir
print "target dir: ", targetdir

if os.path.exists('tmp'):
    shutil.rmtree('tmp')
os.makedirs('tmp')
shutil.copyfile(targetdir + os.path.sep + 'package.xml',
                'tmp' + os.path.sep + 'package.xml')
if os.path.exists(targetdir):
    shutil.rmtree(targetdir)
os.makedirs(targetdir)
shutil.copyfile('tmp' + os.path.sep + 'package.xml',
                targetdir + os.path.sep + 'package.xml')


# Types / Directories
typeToDir = {"ApexClass": "classes",
             "ApexComponent": "components",
             "ApexPage": "pages",
             "ApexTrigger": "triggers",
	         "AppMenu": "appMenus",
	         "ApprovalProcess": "approvalProcesses",
             "AssignmentRule": "assignmentRules",
             "AuraDefinitionBundle": "aura",
             "AutoResponseRules": "autoResponseRules",
	         "Certificate": "certs",
             "CleanDataService": "cleanDataServices",
             "CustomTab": "tabs",
             "Community": "communities",
             "ContentAsset": "contentassets",
             "CustomApplication": "applications",
             "CustomLabel": "labels",
             "CustomMetadata": "customMetadata",
             "CustomObject": "objects",
             "CustomObjectTranslation": "objectTranslations",
	         "CustomSite": "sites",
	         "CustomTab": "tabs",
	         "Document": "documents",
             "Dashboard": "dashboards",
             "DelegateGroup": "delegateGroups",
             "DuplicateRule": "duplicateRules",
             "EmailTemplate": "email",
             "EntitlementProcess": "entitlementProcesses",
             "EscalationRules": "escalationRules",
             "FlexiPage": "flexipages",
             "FlowDefinition": "flowDefinitions",
             "Group": "groups",
	         "GlobalValueSetTranslation": "globalValueSetTranslations",
             "GlobalValueSet": "globalValueSets",
	         "HomePageComponent": "homePageComponents",
	         "HomePageLayout": "homePageLayouts",
	         "Network": "networks",
             "Layout": "layouts",
	         "Letterhead": "letterhead",
             "MatchingRule": "matchingRules",
	         "ManagedTopics": "managedTopics",
	         "MilestoneType": "milestoneTypes",
             "PathAssistant": "pathAssistants",
	         "PermissionSet": "permissionsets",
             "Profile": "profiles",
             "Queue": "queues",
             "QuickAction": "quickActions",
             "Report": "reports",
	         "ReportType": "reportTypes",
	         "Role": "roles",
	         "Settings": "settings",
	         "SharingRules": "sharingRules",
             "SharingCriteriaRule": "sharingRules",
	         "SiteDotCom": "siteDotComSites",
             "StaticResource": "staticresources",
	         "StandardValueSetTranslation": "standardValueSetTranslations",
             "Translations": "translations",
             "Flow": "flows",
             "Workflow": "workflows",
             "WorkflowFieldUpdate": "workflows",
             "WorkflowRule": "workflows",
             "PlatformCachePartition": "cachePartitions",
             "RemoteSiteSetting": "remoteSiteSettings",
             "StandardValueSet":"standardValueSets"}

tree = ET.parse(targetdir + os.path.sep + 'package.xml')
root = tree.getroot()
print root.tag
for child in root.findall('{http://soap.sforce.com/2006/04/metadata}types'):
    print "----------------------"
    print "Child found: "+ child.find('{http://soap.sforce.com/2006/04/metadata}name').text
    foundchild = child.find('{http://soap.sforce.com/2006/04/metadata}name').text
    try:
        currentFolder = typeToDir[child.find(
            '{http://soap.sforce.com/2006/04/metadata}name').text]
        print "Folder: " + currentFolder
        print "--------------"
        if not os.path.exists(targetdir + os.path.sep + currentFolder):
            os.makedirs(targetdir + os.path.sep + currentFolder)

        if foundchild == "AssignmentRule":
            caseRulesFound = False
            leadRulesFound = False
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                    if "Lead" in member.text:
                        leadRulesFound = True
                    if "Case" in member.text:
                        caseRulesFound = True
            if caseRulesFound == True or leadRulesFound == True:
                src = sourcedir +os.path.sep + typeToDir[foundchild] + os.path.sep
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
            if caseRulesFound == True:
                shutil.copy(src+"Case.assignmentRules",tgt)
                print "\t\t\tSrc: "+src+"Case.assignmentRules"
                print "\t\t\tTgt: "+tgt+"Case.assignmentRules"
            if leadRulesFound == True:
                shutil.copy(src+"Lead.assignmentRules",tgt)
                print "\t\t\tSrc: "+src+"Lead.assignmentRules"
                print "\t\t\tTgt: "+tgt+"Lead.assignmentRules"

        elif foundchild == "Dashboard":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                if '/' not in member.text :
                    # Creo el folder para los dashboards, y copio la metadata del propio folder.
                    print "\tDashboard folder: " + member.text
                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + "-meta.xml"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                    os.makedirs(tgt+member.text)
                    shutil.copy(src,tgt)
                else: 
                    dashboardName = member.text.split("/")[1]
                    dashboardPath = member.text.split("/")[0]
                    print "\t\tDashboard name: " + dashboardName
                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + dashboardPath + os.path.sep + dashboardName + ".dashboard"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep + dashboardPath + os.path.sep
                    print "\t\t\tSrc: "+src
                    print "\t\t\tTgt: "+tgt
                    shutil.copy(src,tgt)
    
        elif foundchild == "Report":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                if '/' not in member.text :
                    # Creo el folder para los reports, y copio la metadata del propio folder.
                    print "\tReport folder: " + member.text
                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + "-meta.xml"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                    os.makedirs(tgt+member.text)
                    shutil.copy(src,tgt)
                else: 
                    reportName = member.text.split("/")[1]
                    reportPath = member.text.split("/")[0]
                    print "\t\tReport name: " + reportName
                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + reportPath + os.path.sep + reportName + ".report"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep + reportPath + os.path.sep 
                    print "\t\t\tSrc: "+src
                    print "\t\t\tTgt: "+tgt
                    shutil.copy(src,tgt)
        
        elif foundchild == "EmailTemplate":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                if '/' not in member.text :
                    # Creo el folder para los templates, y copio la metadata del propio folder.
                    print "\tTemplate folder: " + member.text
                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + "-meta.xml"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                    os.makedirs(tgt+member.text)
                    shutil.copy(src,tgt)
                else:
                    templateName = member.text.split("/")[1]
                    templatePath = member.text.split("/")[0]
                    print "\tTemplate name: " + templateName
                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + templatePath + os.path.sep + templateName + ".email"
                    src2 = src + "-meta.xml"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep + templatePath + os.path.sep
                    print "\t\t\tSrc: "+src
                    print "\t\t\tTgt: "+tgt
                    shutil.copy(src,tgt)
                    shutil.copy(src2,tgt)
        
        elif foundchild == "ApexClass":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tClass: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".cls-meta.xml"
                src2 = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".cls"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tSrc2: "+src2
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
                shutil.copy(src2,tgt)

        elif foundchild == "MilestoneType":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tMilestone: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".milestoneType"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "WorkflowRule":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tWorkflowRule: " + member.text
		tipoObjWf=member.text.split('.')[0];
		print "\tObjeto workflow rule: "+tipoObjWf
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + tipoObjWf + ".workflow"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)


        elif foundchild == "WorkflowFieldUpdate":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tWorkflowFieldUpdate: " + member.text
                tipoObjWf=member.text.split('.')[0];
                print "\tObjeto workflow field update: "+tipoObjWf
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + tipoObjWf + ".workflow"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)



        elif foundchild == "ApexPage":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tPage: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".page-meta.xml"
                src2 = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".page"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tSrc2: "+src2
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
                shutil.copy(src2,tgt)
        
        elif foundchild == "ApexComponent":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\ApexComponent: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".component-meta.xml"
                src2 = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".component"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tSrc2: "+src2
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
                shutil.copy(src2,tgt)

        elif foundchild == "CustomObject":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tObject: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".object"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
        
        elif foundchild == "CustomApplication":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\CustomApplication: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".app"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
        
        elif foundchild == "CustomMetadata":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\CustomMetadata: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".md"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
    
        elif foundchild == "ApprovalProcess":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\ApprovalProcess: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".approvalProcess"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        
        elif foundchild == "FlexiPage":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tFlexiPage: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".flexipage"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
        
        elif foundchild == "FlowDefinition":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tFlowDefinition: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".flowDefinition"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
    
        elif foundchild == "Flows":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tFlow: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".flow"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "Group":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tGroup: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".group"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "Layout":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tLayout: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".layout"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
        
        elif foundchild == "CustomObjectTranslation":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tCustomObjectTranslation: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".objectTranslation"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "PathAssistant":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tPathAssistant: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".pathAssistant"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "PermissionSet":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tPermissionSet: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".permissionset"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "Queue":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tQueue: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".queue"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "QuickAction":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tQuickAction: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".quickAction"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "RemoteSiteSetting":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tRemoteSiteSetting: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".remoteSite"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
    
        elif foundchild == "Profile":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tProfile: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".profile"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
    
        elif foundchild == "Role":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tRole: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".role"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)

        elif foundchild == "StaticResource":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tStaticResource: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".resource"
                src2 = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".resource-meta.xml"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
                shutil.copy(src2,tgt)

        elif foundchild == "ApexTrigger":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tTrigger: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".trigger"
                src2 = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".trigger-meta.xml"
                tgt = targetdir + os.path.sep + currentFolder + os.path.sep
                print "\t\t\tSrc: "+src
                print "\t\t\tTgt: "+tgt
                shutil.copy(src,tgt)
                shutil.copy(src2,tgt)

        else:
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tMember: " + member.text
                try:
                    def file_in_folder(argument):
                        switcher = {
                            'labels': 'CustomLabels'
                        }             
                        return switcher.get(argument, "")  

                    if file_in_folder(currentFolder) != "":
                        member.text=file_in_folder(currentFolder)

                    src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + "*"
                    tgt = targetdir + os.path.sep + currentFolder + os.path.sep

		    print "Origen copia: "+src
                    for file1 in glob.glob(src):
                        print "\t\t\tcopy file: ", file1                     
                        shutil.copy(file1, tgt)
                except IOError as e:
                    if (e.errno == 21 or e.errno == 13):
                        shutil.copytree(src[:-1], tgt + os.path.sep + member.text)
                    else:
                        print "IOError({0}): {1}".format(e.errno, e.strerror)
    except KeyError:
        pass

shutil.rmtree('tmp')
