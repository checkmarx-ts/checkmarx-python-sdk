from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
    get_a_list_of_projects,
    get_last_scan_info,
    get_all_scanners_results_by_scan_id
)

import csv
from datetime import datetime

class passwordResult:
  def __init__(self, projectName, tags, type, queryName, severity, fileName, line, language, status, state, foundAt):
    self.projectName = projectName
    self.tags = tags
    self.type = type
    self.queryName = queryName
    self.severity = severity
    self.fileName = fileName
    self.line = line
    self.language = language
    self.status = status
    self.state = state
    self.foundAt = foundAt
  
  def __iter__(self):
    return iter([self.projectName, self.tags, self.type, self.queryName, self.severity, self.fileName, self.line, self.language, self.status, self.state, self.foundAt])

if __name__ == '__main__':

    #get all projects
    allProjects = get_a_list_of_projects(limit=1000)
    allTargetResults = []
    for project in allProjects.projects:
        lastScanInfo = get_last_scan_info(project_ids=[project.id], limit=1)
        scanInfo= lastScanInfo.get(project.id)

        if scanInfo:
            scanData = get_all_scanners_results_by_scan_id(scan_id=scanInfo.id, limit=10000)
            
            #get results from scan that relate to passwords
            allResults = scanData.get("results")

            for result in allResults:
                resultData = result.data
                #add secrets, keys, truffle hog to list of things to look for

                #process sast results
                if result.type == "sast":
                    if "password" in resultData.get("queryName").lower() or "secret" in resultData.get("queryName").lower() or "key" in resultData.get("queryName").lower():
                        targetResult = passwordResult(
                            projectName = project.name,
                            tags = project.tags,
                            type = result.type,
                            queryName = resultData.get("queryName"),
                            severity = result.severity,
                            fileName = resultData.get("nodes")[0].get("fileName"),
                            line = resultData.get("nodes")[0].get("line"),
                            language = resultData.get("languageName"),
                            status = result.status,
                            state = result.state,
                            foundAt = result.foundAt
                        )
                        
                        allTargetResults.append(targetResult)

                #process kics results        
                if result.type == "kics":
                   if "password" in resultData.get("queryName").lower() or "secret" in resultData.get("queryName").lower() or "key" in resultData.get("queryName").lower():
                        targetResult = passwordResult(
                            projectName = project.name,
                            tags = project.tags,
                            type = result.type,
                            queryName = resultData.get("queryName"),
                            severity = result.severity,
                            fileName = resultData.get("fileName"),
                            line = resultData.get("line"),
                            language = resultData.get("platform"),
                            status = result.status,
                            state = result.state,
                            foundAt = result.foundAt
                        )
                        
                        allTargetResults.append(targetResult)
            
        else:
            print("This project has no scans: " + project.name)

        #Create csv file with all results
        currentDate = datetime.now().strftime("%d-%m-%Y")
        fileName = "PasswordFindings_" + currentDate + ".csv"
        csvHeaders = ["projectName", "projectTags", "type", "queryName", "severity", "fileName", "line", "language", "status", "state", "foundAt"]
        with open(fileName, "w") as stream:
            writer = csv.DictWriter(stream, fieldnames=csvHeaders)
            writer.writeheader()
            
            writer = csv.writer(stream)
            writer.writerows(allTargetResults)