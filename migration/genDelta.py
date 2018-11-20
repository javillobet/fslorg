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
             "AssignmentRules": "assignmentRules",
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

        if foundchild == "AssignmentRules":
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
                    print "\t\tTemplate name: " + templateName
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

        elif foundchild == "CustomObject":
            for member in child.findall('{http://soap.sforce.com/2006/04/metadata}members'):
                print "\tObject: " + member.text
                src = sourcedir + os.path.sep + currentFolder + os.path.sep + member.text + ".object"
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

		    print "Source en glob: "+src
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
