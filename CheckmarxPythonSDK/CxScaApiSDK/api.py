from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxScaApiSDK.config import construct_configuration
from typing import List, Union
from requests import Response
import json
import os
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, OK, CREATED, ACCEPTED
from requests_toolbelt import MultipartEncoder
agent_headers = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/106.0.0.0 Safari/537.36",
}


class Sca(object):
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.gql_relative_url = "/graphql/graphql"

    def get_all_projects(self, project_name: str = None) -> Union[dict, List[dict]]:
        """

        Args:
            project_name (str):

        Returns:
            list of dict, or dict if project_name is provided

            Sample:
            [
              {
                'id': '075e6da2-f7cb-43e8-8c94-2fb823d5c29c',
                'name': 'WebGoatKB',
                'isManaged': False,
                'createdOn': '2020-07-22T17:58:30.693057',
                'tenantId': '19',
                'branch': 'master',
                'assignedTeams': ['/CxServer/SCA-PM/Champions/UK'],
                'lastSuccessfulScanId': '8bad3b00-71a8-466b-af24-8a9ea0d170da',
              }
            ]
        """
        url = "/risk-management/projects"
        if project_name:
            url += "?name={project_name}".format(project_name=project_name)

        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def check_if_project_already_exists(self, project_name: str) -> bool:
        """

        Args:
            project_name (str):

        Returns:
            exists (bool)
        """
        all_projects = self.get_all_projects()

        project_name_list = [project.get("name") for project in all_projects]

        if project_name in project_name_list:
            return True

        return False

    def create_a_new_project(self, project_name: str, assigned_teams: List[str] = None) -> dict:
        """

        Args:
            project_name (str):
            assigned_teams (list of str):

        Returns:
            dict

            sample:
            {
              'id': '89ba3807-1d93-4802-a308-ec0ad6641777',
              'name': 'happy_test_2021_01_14',
              'isManaged': False,
              'createdOn': '2021-01-14T08:33:10.7217433Z',
              'tenantId': '19',
              'branch': 'master',
              'assignedTeams': [],
              'lastSuccessfulScanId': None
            }
        """
        if assigned_teams is None:
            assigned_teams = []

        url = "/risk-management/projects"
        data = json.dumps(
            {
                "Name": project_name,
                "AssignedTeams": assigned_teams
            }
        )
        response = self.api_client.post_request(url, data)
        return response.json()

    def get_project_id_by_name(self, project_name: Union[str, List[str]]) -> Union[str, List[str]]:
        """

        Args:
            project_name (str, list of str):

        Returns:
            project_id (str, list of str)
        """
        if isinstance(project_name, str):
            project = self.get_all_projects(project_name=project_name)
            return project.get("id")
        elif isinstance(project_name, list):
            projects = self.get_all_projects()
            return [project.get("id") for project in projects if project.get("name") in project_name]

    def get_project_by_id(self, project_id: str) -> dict:
        """

        Args:
            project_id (str):

        Returns:
            dict
        """
        url = "/risk-management/projects/{id}".format(id=project_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def update_project(self, project_id: str, project_name: str = None, assigned_teams: List[str] = None) -> bool:
        """

        Args:
            project_id (str):
            project_name (str):
            assigned_teams (list of str):

        Returns:
            bool
        """
        result = False
        url = "/risk-management/projects/{id}".format(id=project_id)
        data = {}
        if project_name:
            data.update({"Name": project_name})
        if assigned_teams:
            data.update({"AssignedTeams": assigned_teams})

        data = json.dumps(data)
        response = self.api_client.put_request(relative_url=url, data=data)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def delete_project(self, project_id: str) -> bool:
        """

        Args:
            project_id (str):

        Returns:
            bool
        """
        result = False
        url = "/risk-management/projects/{id}".format(id=project_id)
        response = self.api_client.delete_request(relative_url=url)
        if response.status_code == NO_CONTENT:
            result = True
        return result

    def get_all_scans_associated_with_a_project(self, project_id: str) -> List[dict]:
        """

        Args:
            project_id (str):

        Returns:
            list of dict

            sample:
                [
                 {
                   'projectId': '2e100308-5a58-49ea-a003-dbff3481dc5a',
                   'createdOn': '2021-01-16T15:16:54.676767Z',
                   'lastUpdate': '2021-01-16T15:16:58.078848Z',
                   'status': {'name': 'Done', 'message': None},
                   'origin': 'Zip',
                   'riskReportId': '4187e52d-7dae-4606-9402-72d22295825f',
                   'scanId': '4187e52d-7dae-4606-9402-72d22295825f',
                   'revision': None,
                   'username': 'happyy',
                   'tenantId': '19',
                   'scanProgress': [
                      {
                        'name': 'Downloading source code if absent',
                        'startTime': '2021-01-16T15:16:54.744981Z',
                        'endTime': '2021-01-16T15:16:54.885971Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Evaluate Policies',
                        'startTime': '2021-01-16T15:17:01.085963Z',
                        'endTime': '2021-01-16T15:17:01.365927Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Generating risk report',
                        'startTime': '2021-01-16T15:16:58.145557Z',
                        'endTime': '2021-01-16T15:17:01.067229Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Collecting Evidence',
                        'startTime': '2021-01-16T15:16:54.90395Z',
                        'endTime': '2021-01-16T15:16:57.996994Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Storing Evidence',
                        'startTime': '2021-01-16T15:16:58.030985Z',
                        'endTime': '2021-01-16T15:16:58.049947Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Storing Manifests',
                        'startTime': '2021-01-16T15:16:58.066822Z',
                        'endTime': '2021-01-16T15:16:58.128849Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Generating download link',
                        'startTime': '2021-01-16T15:16:54.69109Z',
                        'endTime': '2021-01-16T15:16:54.728409Z',
                        'status': 'Done'
                      },
                      {
                        'name': 'Collecting Fingerprints',
                        'startTime': '2021-01-16T15:16:58.014002Z',
                        'endTime': '2021-01-16T15:16:58.014068Z',
                        'status': 'Done'
                      }
                   ]
                 }
                ]
        """
        url = "/risk-management/scans?projectId={project_id}".format(project_id=project_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_latest_scan_id_of_a_project(self, project_id: str) -> str:
        """

        Returns:
            scan_id (str)
        """
        scan_id = None
        all_scans = self.get_all_scans_associated_with_a_project(project_id)

        if len(all_scans) > 1:
            all_scans = sorted(all_scans, key=lambda s: s.get("createdOn"))

        if all_scans:
            scan_id = all_scans[-1].get("scanId")

        return scan_id

    def get_scan_by_id(self, scan_id: str) -> dict:
        """

        Args:
            scan_id (str):

        Returns:
            dict

            sample:
            {
               'projectId': '2e100308-5a58-49ea-a003-dbff3481dc5a',
               'createdOn': '2021-01-16T15:16:54.676767Z',
               'lastUpdate': '2021-01-16T15:16:58.078848Z',
               'status': {'name': 'Done', 'message': None},
               'origin': 'Zip',
               'riskReportId': '4187e52d-7dae-4606-9402-72d22295825f',
               'scanId': '4187e52d-7dae-4606-9402-72d22295825f',
               'revision': None,
               'username': 'happyy',
               'tenantId': '19',
               'scanProgress': [
                  {
                    'name': 'Downloading source code if absent',
                    'startTime': '2021-01-16T15:16:54.744981Z',
                    'endTime': '2021-01-16T15:16:54.885971Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Evaluate Policies',
                    'startTime': '2021-01-16T15:17:01.085963Z',
                    'endTime': '2021-01-16T15:17:01.365927Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Generating risk report',
                    'startTime': '2021-01-16T15:16:58.145557Z',
                    'endTime': '2021-01-16T15:17:01.067229Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Collecting Evidence',
                    'startTime': '2021-01-16T15:16:54.90395Z',
                    'endTime': '2021-01-16T15:16:57.996994Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Storing Evidence',
                    'startTime': '2021-01-16T15:16:58.030985Z',
                    'endTime': '2021-01-16T15:16:58.049947Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Storing Manifests',
                    'startTime': '2021-01-16T15:16:58.066822Z',
                    'endTime': '2021-01-16T15:16:58.128849Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Generating download link',
                    'startTime': '2021-01-16T15:16:54.69109Z',
                    'endTime': '2021-01-16T15:16:54.728409Z',
                    'status': 'Done'
                  },
                  {
                    'name': 'Collecting Fingerprints',
                    'startTime': '2021-01-16T15:16:58.014002Z',
                    'endTime': '2021-01-16T15:16:58.014068Z',
                    'status': 'Done'
                  }
               ]
            }
        """
        url = "/risk-management/scans/{scanId}".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_scan_status(self, scan_id: str) -> dict:
        """

        Args:
            scan_id (str):

        Returns:
            dict

            sample: {'name': 'Done', 'message': None}
        """
        url = "/risk-management/scans/{scanId}/status".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_scan_settings(self, scan_id: str) -> dict:
        """

        Args:
            scan_id (str):

        Returns:
            dict

            sample:
                {
                    'enableExploitablePath': False,
                    'sourceControlBranch': 'master',
                    'sourceControlRevision': '8f6b34d64ce39b3fa137ef08d40fb86df7ff8b7c'
                }
        """
        url = "/risk-management/scans/{scanId}/settings".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_risk_report_summary(self, project_id: str = None, size: int = 10, skip: int = 0) -> List[dict]:
        """

        Args:
            project_id (str):
            size (int): default 10
            skip (int): 0

        Returns:
            list of dict

            sample:
                [
                  {
                    'riskReportId': '916f9d08-b0fe-479c-b19e-1d02d6e3f2e8',
                    'projectId': '2e100308-5a58-49ea-a003-dbff3481dc5a',
                    'highVulnerabilityCount': 15,
                    'mediumVulnerabilityCount': 6,
                    'lowVulnerabilityCount': 1,
                    'totalPackages': 15,
                    'directPackages': 6,
                    'createdOn': '2021-01-17T02:00:09.180126Z',
                    'riskScore': 9.800000190734863,
                    'totalOutdatedPackages': 12
                  },
                  {
                    'riskReportId': '4187e52d-7dae-4606-9402-72d22295825f',
                    'projectId': '2e100308-5a58-49ea-a003-dbff3481dc5a',
                    'highVulnerabilityCount': 15,
                    'mediumVulnerabilityCount': 6,
                    'lowVulnerabilityCount': 1,
                    'totalPackages': 15,
                    'directPackages': 6,
                    'createdOn': '2021-01-16T15:17:01.031203Z',
                    'riskScore': 9.800000190734863,
                    'totalOutdatedPackages': 12
                  }
                ]
        """
        url = "/risk-management/risk-reports"

        optionals = []
        if project_id:
            optionals.append("projectId={project_id}".format(project_id=project_id))
        if size:
            optionals.append("size={size}".format(size=size))
        if skip:
            optionals.append("skip={skip}".format(skip=skip))
        if optionals:
            url += "?" + "&".join(optionals)

        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_packages_of_a_scan(self, scan_id: str) -> List[dict]:
        """

        Args:
            scan_id (str):

        Returns:
            list of dict

            sample:
                [
                  {
                    'id': 'Yarn-antlr:antlr-2.7.7',
                    'name': 'antlr:antlr',
                    'version': '2.7.7',
                    'licenses': ['Yarn-antlr:antlr-2.7.7-BSD 3'],
                    'matchType': 'Filename',
                    'highVulnerabilityCount': 0,
                    'mediumVulnerabilityCount': 0,
                    'lowVulnerabilityCount': 0,
                    'ignoredVulnerabilityCount': 0,
                    'numberOfVersionsSinceLastUpdate': 2,
                    'newestVersionReleaseDate': '2007-01-14T01:30:51',
                    'newestVersion': '3.0b5',
                    'outdated': True,
                    'releaseDate': '2007-01-13T06:28:39',
                    'confidenceLevel': '100',
                    'riskScore': 0.0,
                    'severity': 'NONE',
                    'locations': ['pom.xml'],
                    'dependencyPaths': [
                      [
                        {
                          'id': 'Yarn-org.hibernate:hibernate-core-4.0.1.Final',
                          'name': 'org.hibernate:hibernate-core',
                          'version': '4.0.1.Final',
                          'isResolved': True,
                          'isDevelopment': False
                        },
                        {
                          'id': 'Yarn-antlr:antlr-2.7.7',
                          'name': 'antlr:antlr',
                          'version': '2.7.7',
                          'isResolved': True,
                          'isDevelopment': False
                        }
                      ]
                    ],
                    'packageRepository': 'Maven',
                    'isDirectDependency': False,
                    'isDevelopment': False,
                    'packageUsage': {
                      'usageType': 'UnScanned',
                      'packageId': None,
                      'importsCalled': [],
                      'methodsCalled': [],
                      'packageUsageComplexity': -1.0
                    }
                  },
                  {
                    'id': 'Yarn-commons-collections:commons-collections-3.2.1',
                    'name': 'commons-collections:commons-collections',
                    'version': '3.2.1',
                    'licenses': ['Yarn-commons-collections:commons-collections-3.2.1-Apache 2.0'],
                    'matchType': 'Filename',
                    'highVulnerabilityCount': 3,
                    'mediumVulnerabilityCount': 0,
                    'lowVulnerabilityCount': 0,
                    'ignoredVulnerabilityCount': 0,
                    'numberOfVersionsSinceLastUpdate': 1,
                    'newestVersionReleaseDate': '2015-11-12T23:11:26',
                    'newestVersion': '3.2.2',
                    'outdated': True,
                    'releaseDate': '2008-04-15T01:09:24',
                    'confidenceLevel': '100',
                    'riskScore': 9.800000190734863,
                    'severity': 'HIGH',
                    'locations': ['pom.xml'],
                    'dependencyPaths': [
                      [
                        {
                          'id': 'Yarn-org.hibernate:hibernate-core-4.0.1.Final',
                          'name': 'org.hibernate:hibernate-core',
                          'version': '4.0.1.Final',
                          'isResolved': True,
                          'isDevelopment': False
                        },
                        {
                          'id': 'Yarn-commons-collections:commons-collections-3.2.1',
                          'name': 'commons-collections:commons-collections',
                          'version': '3.2.1',
                          'isResolved': True,
                          'isDevelopment': False
                        }
                      ]
                    ],
                    'packageRepository': 'Maven',
                    'isDirectDependency': False,
                    'isDevelopment': False,
                    'packageUsage': {
                      'usageType': 'UnScanned',
                      'packageId': None,
                      'importsCalled': [],
                      'methodsCalled': [],
                      'packageUsageComplexity': -1.0
                    }
                  },
                  {
                    'id': 'Yarn-dom4j:dom4j-1.6.1',
                    'name': 'dom4j:dom4j',
                    'version': '1.6.1',
                    'licenses': [],
                    'matchType': 'Filename',
                    'highVulnerabilityCount': 2,
                    'mediumVulnerabilityCount': 0,
                    'lowVulnerabilityCount': 0,
                    'ignoredVulnerabilityCount': 0,
                    'numberOfVersionsSinceLastUpdate': 0,
                    'newestVersionReleaseDate': None,
                    'newestVersion': None,
                    'outdated': False,
                    'releaseDate': '2006-02-10T12:33:18',
                    'confidenceLevel': '100',
                    'riskScore': 9.800000190734863,
                    'severity': 'HIGH',
                    'locations': ['pom.xml'],
                    'dependencyPaths': [
                      [
                        {
                          'id': 'Yarn-org.hibernate:hibernate-core-4.0.1.Final',
                          'name': 'org.hibernate:hibernate-core',
                          'version': '4.0.1.Final',
                          'isResolved': True,
                          'isDevelopment': False
                        },
                        {
                          'id': 'Yarn-dom4j:dom4j-1.6.1',
                          'name': 'dom4j:dom4j',
                          'version': '1.6.1',
                          'isResolved': True,
                          'isDevelopment': False
                        }
                      ]
                    ],
                    'packageRepository': 'Maven',
                    'isDirectDependency': False,
                    'isDevelopment': False,
                    'packageUsage': {
                      'usageType': 'UnScanned',
                      'packageId': None,
                      'importsCalled': [],
                      'methodsCalled': [],
                      'packageUsageComplexity': -1.0
                    }
                  }
                ]

        """
        url = "/risk-management/risk-reports/{scanId}/packages".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_vulnerabilities_of_a_scan(self, scan_id: str) -> List[dict]:
        """

        Args:
            scan_id (str):

        Returns:
            list of dict

            sample:
                [
                  {
                    'id': 'CVE-2015-7501', 'cveName': 'CVE-2015-7501', 'score': 9.8, 'severity': 'High',
                    'publishDate': '2017-11-09T17:29:00', 'references': [], 'referencesData': [],
                    'description': 'Red Hat JBoss A-MQ 6.x; BPM Suite (BPMS) 6.x; BRMS 6.x and 5.x; Data Grid (JDG) 6.x;
                             Data Virtualization (JDV) 6.x and 5.x; Enterprise Application Platform 6.x, 5.x, and 4.3.x;
                             Fuse 6.x; Fuse Service Works (FSW) 6.x; Operations Network (JBoss ON) 3.x; Portal 6.x;
                             SOA Platform (SOA-P) 5.x; Web Server (JWS) 3.x; Red Hat OpenShift/xPAAS 3.x;
                             and Red Hat Subscription Asset Manager 1.3 allow remote attackers to execute arbitrary
                             commands via a crafted serialized Java object,
                             related to the Apache Commons Collections (ACC) library.',
                    'cvss': {
                      'version': 3.0, 'attackVector': 'NETWORK', 'attackComplexity': 'LOW',
                      'confidentiality': 'HIGH', 'availability': 'HIGH', 'integrityImpact': 'HIGH',
                      'authentication': None
                    },
                    'recommendations': None, 'packageId': 'Yarn-commons-collections:commons-collections-3.2.1',
                    'similarityId': None, 'fixResolutionText': '3.2.2', 'isIgnored': False, 'exploitableMethods': [],
                    'cwe': 'CWE-502'
                  },
                  {
                    'id': 'Cx78f40514-81ff', 'cveName': '', 'score': 7.5, 'severity': 'High',
                    'publishDate': '2018-10-31T10:39:00',
                    'references': [
                      'https://issues.apache.org/jira/browse/COLLECTIONS-701',
                      'https://github.com/apache/commons-collections/pull/57',
                      'https://github.com/apache/commons-collections/commit/1979a6e31067a18c9ede59ad4518f738512eba82'
                    ],
                    'referencesData': [
                      {'url': 'https://issues.apache.org/jira/browse/COLLECTIONS-701', 'type': 'Issue', 'comment': ''},
                      {'url': 'https://github.com/apache/commons-collections/pull/57', 'type': 'Pull request',
                      'comment': ''},
                      {'url': 'https://github.com/apache/commons-collections/commit/1979a6e31067a18c9ede59ad4518f73851
                              2eba82',
                      'type': 'Commit', 'comment': ''}
                    ],
                    'description': 'The framework Apache Commons Collections before 4.3 is vulnerable to\nStack
                    Overflow.
                      The function `add()` in the file `src/main/java/org/apache/commons/collections4/list/
                      SetUniqueList.java` throws a StackOverflowError when the `add()`
                      method is called with its own list.\nTo resolve this issue - upgrade to version 4.3.
                      Please note: the package name was changed to org.apache.commons:commons-collections4
                      on version 4.0.',
                    'cvss': {'version': 3.0, 'attackVector': 'NETWORK', 'attackComplexity': 'LOW',
                      'confidentiality': 'NONE', 'availability': 'HIGH', 'integrityImpact': 'NONE',
                      'authentication': None},
                    'recommendations': None,
                    'packageId': 'Yarn-commons-collections:commons-collections-3.2.1', 'similarityId': None,
                    'fixResolutionText': '', 'isIgnored': False, 'exploitableMethods': [], 'cwe': 'CWE-674'
                  }
                ]
        """
        url = "/risk-management/risk-reports/{scanId}/vulnerabilities".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_licenses_of_a_scan(self, scan_id: str) -> List[dict]:
        """

        Args:
            scan_id (str):

        Returns:
            list of dict
            sample:
            [
              {
                'id': 'Yarn-antlr:antlr-2.7.7-BSD 3',
                'referenceType': 'PomFile',
                'reference': 'https://mvnrepository.com/artifact/antlr/antlr/2.7.7',
                'royaltyFree': 'Free',
                'copyrightRiskScore': 3,
                'riskLevel': 'Low',
                'linking': 'NonViral',
                'copyLeft': 'NoCopyleft',
                'patentRiskScore': 3,
                'name': 'BSD 3',
                'url': 'https://opensource.org/licenses/BSD-3-Clause',
               }
            ]
        """
        url = "/risk-management/risk-reports/{scanId}/licenses".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_warnings_of_a_scan(self, scan_id: str) -> List[dict]:
        """

        Args:
            scan_id (str):

        Returns:
            list of dict

            sample:
                [
                  {
                    "warningCode": "FailedToResolve",
                    "affectedFiles": [
                      "application\\build.gradle"
                    ]
                  }
                ]
        """
        url = "/risk-management/risk-reports/{scanId}/warnings".format(scanId=scan_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def ignore_a_vulnerability_for_a_specific_package_and_project(
            self, project_id: str, vulnerability_id: str, package_id: str
    ) -> bool:
        """

        Args:
            project_id (str):
            vulnerability_id (str):
            package_id (str):

        Returns:
            is_successful (bool)
        """
        is_successful = False
        url = "/risk-management/risk-reports/IgnoreVulnerability"
        data = json.dumps(
            {
                "ProjectId": project_id,
                "VulnerabilityId": vulnerability_id,
                "PackageId": package_id
            }
        )
        response = self.api_client.put_request(relative_url=url, data=data)
        if response.status_code == NO_CONTENT:
            is_successful = True
        return is_successful

    def undo_the_ignore_state_of_an_ignored_vulnerability(
            self, project_id: str, vulnerability_id: str, package_id: str
    ) -> bool:
        """

        Args:
            project_id (str):
            vulnerability_id (str):
            package_id (str):

        Returns:
            is_successful (bool)
        """
        is_successful = False
        url = "/risk-management/risk-reports/UnIgnoreVulnerability"
        data = json.dumps(
            {
                "ProjectId": project_id,
                "VulnerabilityId": vulnerability_id,
                "PackageId": package_id
            }
        )
        response = self.api_client.put_request(relative_url=url, data=data)
        if response.status_code == NO_CONTENT:
            is_successful = True
        return is_successful

    def get_settings_for_a_specific_project(self, project_id: str) -> dict:
        """

        Args:
            project_id (str):

        Returns:
            dict

            sample:
            {'enableExploitablePath': False}
        """
        url = "/risk-management/settings/projects/{projectId}".format(projectId=project_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def update_settings_for_a_specific_project(self, project_id: str, enable_exploitable_path: bool) -> bool:
        """

        Args:
            project_id (str):
            enable_exploitable_path (bool):

        Returns:
            is_successful (bool)
        """
        is_successful = False
        url = "/risk-management/settings/projects/{projectId}".format(projectId=project_id)
        data = json.dumps(
            {
                "EnableExploitablePath": enable_exploitable_path
            }
        )
        response = self.api_client.put_request(relative_url=url, data=data)
        if response.status_code == NO_CONTENT:
            is_successful = True
        return is_successful

    def generate_upload_link_for_scanning(self, project_id: str) -> str:
        """
            This function should be used together with the following functions:
                * upload_zip_content_for_scanning
                * scan_previously_uploaded_zip
        Args:
            project_id (str):

        Returns:
            uploadUrl (str)

        """
        url = "/scan-runner/scans/generate-upload-link"
        data = json.dumps(
            {
                "projectId": project_id
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.json().get("uploadUrl")

    def upload_zip_content_for_scanning(self, upload_link, zip_file_path) -> bool:
        """
            This function should be used together with the following functions:
                * generate_upload_link_for_scanning
                * scan_previously_uploaded_zip
        Args:
            upload_link (str):
            zip_file_path (str):

        Returns:
            is_successful (bool)
        """
        is_successful = False

        url = "{uploadLink}".format(uploadLink=upload_link)

        with open(zip_file_path, 'rb') as data:
            response = self.api_client.call_api(method="PUT", url=url, data=data)
            if response.status_code == OK:
                is_successful = True

        return is_successful

    def scan_previously_uploaded_zip(self, project_id: str, uploaded_file_url: str) -> str:
        """
            This function should be used together with the following functions:
                * generate_upload_link_for_scanning
                * upload_zip_content_for_scanning
        Args:
            project_id (str):
            uploaded_file_url (str):

        Returns:
            scanId (str)
        """
        url = "/scan-runner/scans/uploaded-zip"

        data = json.dumps(
            {
                "projectId": project_id,
                "uploadedFileUrl": uploaded_file_url
            }
        )

        response = self.api_client.post_request(relative_url=url, data=data)
        return response.json().get("scanId")

    def generate_upload_link(self) -> str:
        """
            This function should be used together with the following functions:
                * upload_zip_file
                * scan_zip_file_or_github_file

        Returns:
           uploadUrl (str)
        """
        url = "/api/uploads"
        response = self.api_client.post_request(relative_url=url, data=None)
        return response.json().get("url")

    def upload_zip_file(self, upload_link: str, zip_file_path: str) -> bool:
        """
                This function should be used together with the following functions:
                * generate_upload_link
                * scan_zip_file_or_github_file
        Args:
            upload_link (str):
            zip_file_path (str):

        Returns:

        """
        is_successful = False

        url = "{uploadLink}".format(uploadLink=upload_link)

        with open(zip_file_path, 'rb') as data:
            response = self.api_client.call_api(method="PUT", url=url, data=data)
            if response.status_code == OK:
                is_successful = True

        return is_successful

    def scan_zip_file_or_github_file(self, project_id: str, project_type: str, handler_url: str) -> str:
        """
            This function should be used together with the following functions:
                * generate_upload_link
                * upload_zip_file
        Args:
            project_id (str): 	The unique identifier of the Project.
            project_type (str): The Type of Project being scanned, options are:
                    “git” if the Project source code is located in a Git repository.
                    “upload” if the Project source code is stored locally in a zip file.
            handler_url (str):
                    The Git url, or the upload_url that was generated by the POST Generate Upload Link request.
        Returns:
            scan_id (str)
        """
        url = "/api/scans"
        result = None

        if project_type not in ["git", "upload"]:
            raise ValueError("project_type should be git or upload")

        response = self.api_client.post_request(relative_url=url, data=json.dumps({
            "project": {
                "id": f"{project_id}",
                "type": f"{project_type}",
                "handler": {
                    "url": f"{handler_url}"
                }
            }
        }))
        if response.status_code == CREATED:
            result = response.json().get("id")
        return result

    def get_comments_associated_with_a_project(self, project_id: str) -> List[dict]:
        """
        Args:
            project_id (str):
        Returns:
            list of dict
            sample:
                [
                  {
                    "projectId": "2e100308-5a58-49ea-a003-dbff3481dc5a",
                    "vulnerabilityId": "CVE-2015-7501",
                    "packageId": "Yarn-commons-collections:commons-collections-3.2.1",
                    "comment": "new test",
                    "username": "mynewpseudo",
                    "createdOn": "2022-07-18T10:02:14.57846"
                  },
                  {
                    "projectId": "2e100308-5a58-49ea-a003-dbff3481dc5a",
                    "vulnerabilityId": "Cx78f40514-81ff",
                    "packageId": "Yarn-commons-collections:commons-collections-3.2.1",
                    "comment": "test on another vulnId",
                    "username": "mynewpseudo",
                    "createdOn": "2022-07-19T10:13:55.591269"
                  }
                ]
        """

        url = "/risk-management/risk-metadata/{projectId}".format(projectId=project_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def comment_a_vulnerability_for_a_specific_package_and_project(
            self, project_id: str, vulnerability_id: str, package_id: str, comment: str
    ) -> bool:
        """
        Args:
            project_id (str):
            vulnerability_id (str):
            package_id (str):
            comment (str):
        Returns:
            is_successful (bool)
        """
        is_successful = False
        url = "/risk-management/risk-metadata"
        data = json.dumps(
            {
                "projectId": project_id,
                "packageId": package_id,
                "vulnerabilityId": vulnerability_id,
                "comment": comment,
                "username": "NOT USED"
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            is_successful = True
        return is_successful

    def get_states_associated_with_a_project(self, project_id: str) -> List[dict]:
        """
        Args:
            project_id (str):
        Returns:
            list of dict
            sample:
                [
                  {
                    "projectId": "2e100308-5a58-49ea-a003-dbff3481dc5a",
                    "packageId": "Yarn-commons-collections:commons-collections-3.2.1",
                    "vulnerabilityId": "CVE-2015-7501",
                    "state": "ToVerify",
                    "createdOn": "2022-07-18T10:02:14.57846"
                  },
                  {
                    "projectId": "2e100308-5a58-49ea-a003-dbff3481dc5a",
                    "packageId": "Yarn-commons-collections:commons-collections-3.2.1",
                    "vulnerabilityId": "Cx78f40514-81ff",
                    "state": "NotExploitable",
                    "createdOn": "2022-07-19T10:13:55.591269"
                  }
                ]
        """

        url = "/risk-management/risk-state/{projectId}".format(projectId=project_id)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def change_state_of_a_vulnerability_for_a_specific_package_and_project(
            self, project_id: str, vulnerability_id: str, package_id: str, state: str
    ) -> bool:
        """
        Args:
            project_id (str):
            vulnerability_id (str):
            package_id (str):
            state (str):
        Returns:
            is_successful (bool)
        """
        is_successful = False
        url = "/risk-management/risk-state"
        data = json.dumps(
            {
                "packageId": package_id,
                "projectId": project_id,
                "state": state,
                "vulnerabilityId": vulnerability_id
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            is_successful = True
        return is_successful

    def get_scan_reports(self, scan_id: str, report_format: str = "Json", data_types: List[str] = ("All",)) -> bytes:
        """

        Args:
            scan_id (str): The unique identifier of the scan for which you would like to generate a report.
            report_format (str): The format of the report that is generated. Your selection determines whether
                 the report
                 generated is a Scan Report or an SBOM Report. It al determines the file format of the report.
                 Json - Scan Report in JSON format
                 Xml - Scan Report in XML format
                 Pdf - Scan Report in PDF format
                 Csv - Scan Report in CSV format  - for this format, the response is given as a zip file,
                    which can be extracted to obtain the CSV files
                 CycloneDxJson - SBOM report CycloneDX v1.3 format, returned as a JSON
                 CycloneDxXml - SBOM report CycloneDX v1.3 format, returned as an XML
            data_types (list of str, tuple of str):Specifies the sections that will be included in the report.
                You can specify This parameter is relevant only for Scan Reports, not for SBOM Reports.

                 All
                 Packages
                 Vulnerabilities
                 Licenses
                 Policies
                 SupplyChainRisks

        Returns:
            bytes
        """
        if report_format not in ["Json", "Xml", "Pdf", "Csv", "CycloneDxJson", "CycloneDxXml"]:
            raise ValueError("parameter report_format can only be Json, Xml, Pdf, Csv, CycloneDxJson, or CycloneDxXml")
        if data_types and not isinstance(data_types, (list, tuple)):
            raise ValueError("parameter data_types can only be list or tuple")
        for item in data_types:
            if item not in ["All", "Packages", "Vulnerabilities", "Licenses", "Policies", "SupplyChainRisks"]:
                raise ValueError("dataType can only be All, Packages, Vulnerabilities, Licenses, Policies, "
                                 "SupplyChainRisks")
        url = "/risk-management/risk-reports/{scan_id}/export".format(scan_id=scan_id)
        url += "?format={report_format}".format(report_format=report_format)
        url += "".join(["&dataType[]={}".format(data_type) for data_type in data_types])
        response = self.api_client.get_request(relative_url=url)
        return response.content

    def get_aggregated_risks(self, package_type: str, package_name: str, version: str) -> dict:
        """
            This is a public API
        Args:
            package_type (str): e.g. Python
            package_name:
            version:

        Returns:
            dict
        """
        url = "/public/risk-aggregation/aggregated-risks"
        data = json.dumps({
            "packageName": package_name,
            "version": version,
            "packageManager": package_type
        })
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.json()

    def get_artifact_license(self, package_type: str, package_name: str, version: str) -> dict:
        """
            This is a public API
        Args:
            package_type (str): e.g. Python
            package_name:
            version:

        Returns:
            dict
        """
        url = "/public/packages/{}/{}/versions/{}/licenses".format(package_type, package_name, version)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_artifact_info(self, package_type: str, package_name: str, version: str) -> dict:
        """
            This is a public API
        Args:
            package_type (str): e.g.  Python
            package_name:
            version:

        Returns:
            dict
        """
        url = "/public/packages/{}/{}/versions/{}".format(package_type, package_name, version)
        response = self.api_client.get_request(relative_url=url)
        return response.json()

    def get_suggest_private_package(self, package_type: str, package_name: str, version: str) -> dict:
        """
            This is a public API
        Args:
            package_type (str):  Python
            package_name:
            version:

        Returns:

        """
        url = "/private-dependencies-repository/dependencies"
        data = json.dumps([{
            "origin": "PrivateArtifactory",
            "packageManager": package_type,
            "name": package_name,
            "version": version
        }])
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.json()

    def execute_action_on_package_vulnerabilities(
            self, package_name: str, package_manager: str, vulnerability_id: str,
            package_version: str, project_ids: List[str], actions: List[dict]
    ) -> bool:
        """

        action is a dict with the following keys:
        "actionType": "ChangeState"
        "value": "ToVerify", "Confirmed", "Urgent", "NotExploitable"
        "comment":

        Args:
            package_name (str): "handlebars"
            package_manager (str): "npm"
            vulnerability_id (str): "CVE-2019-19919"
            package_version (str): "4.0.5"
            project_ids (list of str):  ["8cce1a5f-b59e-49c4-bff4-f0d709381f01"]
            actions (list of dict):  [
                {
                  "actionType": "ChangeState",
                  "value": "NotExploitable",
                  "comment": "Comment.",
                }
              ]

        Returns:
            bool
        """
        url = "/management-of-risk/package-vulnerabilities"
        data = json.dumps(
            {
                "packageName": package_name,
                "packageManager": package_manager,
                "vulnerabilityId": vulnerability_id,
                "packageVersion": package_version,
                "projectIds": project_ids,
                "actions": actions
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.status_code == CREATED

    def evaluate_package_vulnerabilities(self, scan_id: str, entities: List[dict]) -> List[dict]:
        """

        entity is a dict with the following keys:
        "packageName": package_name,
        "packageVersion": package_version,
        "packageManager": package_manager,
        "vulnerabilityId": vulnerability_id

        Args:
            scan_id (str):
            entities (list of dict):

        Returns:

            [
              {
                "originalEntity": {
                    "packageName": "handlebars",
                    "packageVersion": "4.0.5",
                    "packageManager": "Npm",
                    "vulnerabilityId": "CVE-2019-19919"
                },
                "entityModifications": {
                    "state": "NotExploitable",
                    "isIgnored": true
                },
                "entityProfilesApplied": [
                  "8cce1a5f-b59e-49c4-bff4-f0d709381f01"
                ]
              }
            ]

        """
        result = None
        url = "/management-of-risk/evaluate/package-vulnerabilities"
        data = json.dumps(
            {
                "scanId": scan_id,
                "entities": entities
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def disable_an_action_of_package_vulnerability(
            self, package_name: str, package_version: str, package_manager: str,
            vulnerability_id: str, project_ids: List[str], action_type: str
    ) -> bool:
        """

        Args:
            package_name (str):
            package_version (str):
            package_manager (str):
            vulnerability_id (str):
            project_ids (list of str):
            action_type (str):  "ChangeState", "Snooze", "Ignore", "ChangeScore", "ChangeSeverity",
                "MarkLicenseAsEffective", "AddLicense", "RemoveLicense"

        Returns:
            bool
        """
        result = False
        url = "/management-of-risk/package-vulnerabilities/disable"
        data = json.dumps(
            {
                "packageName": package_name,
                "packageVersion": package_version,
                "packageManager": package_manager,
                "vulnerabilityId": vulnerability_id,
                "projectIds": project_ids,
                "actionType": action_type
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.status_code == NO_CONTENT

    def get_changes_of_package_vulnerabilities_of_a_project(
            self, project_id: str, from_when: str, skip: int, take: int
    ) -> dict:
        """

        Args:
            project_id (str):
            from_when (str): example, "2023-06-17T13:13:30.184592+00:00"
            skip (int): 0
            take (int): 100

        Returns:

        {
          "currentPage": 0,
          "totalPages": 0,
          "pageSize": 100,
          "totalCount": 1,
          "items": [
            {
              "entityProfileId": "8cce1a5f-b59e-49c4-bff4-f0d709381f01",
              "context": {
                "packageName": "handlebars",
                "packageManager": "Npm",
                "packageVersion": "4.0.5",
                "vulnerabilityId": "CVE-2019-19919"
              }
            }
          ]
        }

        """
        result = None
        url = "/management-of-risk/package-vulnerabilities/changes"
        data = json.dumps(
            {
                "projectId": project_id,
                "from": from_when,
                "skip": skip,
                "take": take
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def search_entity_profile_of_package_vulnerabilities(
            self, package_name: str, package_version: str, package_manager: str,
            vulnerability_id: str, project_id: str, action_type: str, to_when: str
    ) -> dict:
        """

        Args:
            package_name (str):
            package_version (str):
            package_manager (str):
            vulnerability_id (str):
            project_id (str):
            action_type (str):  possible values,"ChangeState", "Snooze", "Ignore", "ChangeScore", "ChangeSeverity",
                "MarkLicenseAsEffective", "AddLicense", "RemoveLicense"
            to_when (str):

        Returns:

            {
              "id": "8cce1a5f-b59e-49c4-bff4-f0d709381f01",
              "context": {
                "packageName": "handlebars",
                "packageVersion": "4.0.5",
                "packageManager": "Npm",
                "vulnerabilityId": "CVE-2019-19919"
              },
              "name": "handlebars:4.0.5:Npm:CVE-2019-19919",
              "actions": [
                {
                  "actionType": "ChangeState",
                  "actionValue": "NotExploitable",
                  "enabled": true,
                  "commentContext": {
                    "ManagementOfRiskCommentId": "8cce1a5f-b59e-49c4-bff4-f0d709381f01"
                  },
                  "createdAt": "2023-07-13T18:31:30.849484+00:00"
                }
              ],
              "entityType": "PackageVulnerability",
              "enabled": true,
              "createdAt": "2023-03-23T09:16:54.982Z"
            }
        """
        result = None
        url = "/management-of-risk/package-vulnerabilities/entity-profile/search"
        data = json.dumps(
            {
                "packageName": package_name,
                "packageVersion": package_version,
                "packageManager": package_manager,
                "vulnerabilityId": vulnerability_id,
                "projectId": project_id,
                "actionType": action_type,
                "to": to_when
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def execute_actions_on_supply_chain_risks(
            self, package_name: str, package_manager: str, supply_chain_risk_id: str,
            package_version: str, project_ids: List[str], actions: List[dict]
    ) -> bool:
        """

         action is a dict with the following keys:
        "actionType": "ChangeState"
        "value": "ToVerify", "Confirmed", "Urgent", "NotExploitable"
        "comment":

        Args:
            package_name (str):
            package_manager (str):
            supply_chain_risk_id (str):
            package_version (str):
            project_ids (list of str):
            actions (list of dict):

        Returns:
            bool
        """

        result = False
        url = "/management-of-risk/package-supply-chain-risks"
        data = json.dumps(
            {
                "packageName": package_name,
                "packageManager": package_manager,
                "supplyChainRiskId": supply_chain_risk_id,
                "packageVersion": package_version,
                "projectIds": project_ids,
                "actions": actions
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.status_code == CREATED

    def evaluate_supply_chain_risks(self, scan_id: str, entities: List[str]) -> List[dict]:
        """

        entity is a dict with the following keys:
        "packageName": "handlebars",
        "packageVersion": "4.0.5",
        "packageManager": "Npm",
        "supplyChainRiskId": "Cx3a0295c5-2d04"

        Args:
            scan_id (str):
            entities (list of dict):

        Returns:

            [
              {
                "originalEntity": {
                    "packageName": "handlebars",
                    "packageVersion": "4.0.5",
                    "packageManager": "Npm",
                    "vulnerabilityId": "Cx3a0295c5-2d04"
                },
                "entityModifications": {
                    "state": "NotExploitable",
                    "isIgnored": true
                },
                "entityProfilesApplied": [
                  "8cce1a5f-b59e-49c4-bff4-f0d709381f01"
                ]
              }
            ]
        """
        result = None
        url = "/management-of-risk/evaluate/package-supply-chain-risks"
        data = json.dumps(
            {
                "scanId": scan_id,
                "entities": entities
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == CREATED:
            result = response.json()
        return result

    def disable_an_action_for_a_supply_chain_risk(
            self, package_name: str, package_version: str, package_manager: str,
            supply_chain_risk_id: str, project_ids: List[str], action_type:str
    ) -> bool:
        """

        Args:
            package_name (str):
            package_version (str):
            package_manager (str):
            supply_chain_risk_id (str):
            project_ids (list of str):
            action_type (str): "ChangeState"

        Returns:
            bool
        """
        result = False
        url = "/management-of-risk/package-supply-chain-risks/disable"
        data = json.dumps(
            {
                "packageName": package_name,
                "packageVersion": package_version,
                "packageManager": package_manager,
                "supplyChainRiskId": supply_chain_risk_id,
                "projectIds": project_ids,
                "actionType": action_type
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        return response.status_code == NO_CONTENT

    def get_changes_of_supply_chain_risk(self, project_id: str, from_when: str, skip: int, take: int) -> dict:
        """

        Args:
            project_id (str):
            from_when (str): "2023-06-17T13:13:30.184592+00:00"
            skip (int):  0
            take (int):  100

        Returns:
            {
              "currentPage": 0,
              "totalPages": 0,
              "pageSize": 100,
              "totalCount": 1,
              "items": [
                {
                  "entityProfileId": "8cce1a5f-b59e-49c4-bff4-f0d709381f01",
                  "context": {
                    "packageName": "handlebars",
                    "packageManager": "Npm",
                    "packageVersion": "4.0.5",
                    "supplyChainRiskId": "Cx3a0295c5-2d04",
                  }
                }
              ]
            }
        """
        result = None
        url = "/management-of-risk/package-supply-chain-risks/changes"
        data = json.dumps(
            {
                "projectId": project_id,
                "from": from_when,
                "skip": skip,
                "take": take
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def search_entity_profile_of_package_supply_chain_risks(
            self, package_name: str, package_version: str, package_manager: str,
            supply_chain_risk_id: str, project_id: str, action_type: str, to_when: str
    ) -> dict:
        """

        Args:
            package_name (str):
            package_version (str):
            package_manager (str):
            supply_chain_risk_id (str):
            project_id (str):
            action_type (str):
            to_when (str):

        Returns:
            {
              "id": "8cce1a5f-b59e-49c4-bff4-f0d709381f01",
              "context": {
                "packageName": "handlebars",
                "packageVersion": "4.0.5",
                "packageManager": "Npm",
                "supplyChainRiskId": "Cx3a0295c5-2d04",
              },
              "name": "handlebars:4.0.5:Npm:CVE-2019-19919",
              "actions": [
                {
                  "actionType": "ChangeState",
                  "actionValue": "NotExploitable",
                  "enabled": true,
                  "commentContext": {
                    "ManagementOfRiskCommentId": "8cce1a5f-b59e-49c4-bff4-f0d709381f01"
                  },
                  "createdAt": "2023-07-13T18:31:30.849484+00:00"
                }
              ],
              "entityType": "PackageSupplyChainRisk",
              "enabled": true,
              "createdAt": "2023-03-23T09:16:54.982Z"
            }
        """
        result = None
        url = "/management-of-risk/package-supply-chain-risks/entity-profile/search"
        data = json.dumps(
            {
                "packageName": package_name,
                "packageVersion": package_version,
                "packageManager": package_manager,
                "supplyChainRiskId": supply_chain_risk_id,
                "projectId": project_id,
                "actionType": action_type,
                "to": to_when
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def execute_actions_on_package_license(
            self, package_id: str, license_name: str, project_ids: str, actions: List[dict]
    ) -> bool:
        """

        action is a dict with following keys:
        "actionType": "MarkLicenseAsEffective",
        "value": "MarkLicenseAsEffective",
        "comment": "Comment."

        Args:
            package_id (str):
            license_name (str):
            project_ids (list of str):
            actions (list of dict):

        Returns:
            bool
        """
        result = False
        url = "/management-of-risk/package-licenses"
        data = json.dumps(
            {
                "packageId": package_id,
                "licenseName": license_name,
                "projectIds": project_ids,
                "actions": actions
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == CREATED:
            result = True
        return result

    def evaluate_package_licenses(self, entities: List[dict], scan_id: str) -> List[dict]:
        """

        entity is a dict: for example
        {
            "package":
            {
                "packageId": "npm-handlebars-4.0.5"
            },
            "identifiedLicenses": [
                {
                    "license":
                    {
                        "name": "apache2"
                    }
                }
            ]
        }

        Args:
            entities (list of dict):
            scan_id (str):

        Returns:
            [
              {
                "originalEntity": {
                  "package": {
                    "packageId": "npm-handlebars-4.0.5"
                  },
                  "identifiedLicenses": [
                    {
                      "license": {
                        "name": "apache2"
                      }
                    }
                  ]
                },
                "entityModifications": {
                  "licenseNames": [
                    "MarkLicenseAsEffective"
                  ],
                  "isEffective": true
                },
                "entityProfilesApplied": [
                  "8cce1a5f-b59e-49c4-bff4-f0d709381f01"
                ]
              }
            ]
        """
        result = None
        url = "/management-of-risk/evaluate/package-licenses"
        data = json.dumps(
            {
                "entities": entities,
                "scanId": scan_id
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def search_entity_profiles_of_package_licenses(
            self, package_id: str, license_name: str, project_id: str, action_type: str, to_when: str
    ) -> dict:
        """

        Args:
            package_id (str):
            license_name (str):
            project_id (str):
            action_type (str):
            to_when (str):

        Returns:
            {
              "id": "8cce1a5f-b59e-49c4-bff4-f0d709381f0a",
              "context": {
                "LicenseName": "apache2",
                "PackageId": "npm-handlebars-4.0.5"
              },
              "name": "package-xpto:Apache2",
              "actions": [
                {
                  "actionType": "MarkLicenseAsEffective",
                  "actionValue": "MarkLicenseAsEffective",
                  "enabled": true,
                  "commentContext": {
                    "ManagementOfRiskCommentId": "8cce1a5f-b59e-49c4-bff4-f0d709381f0a"
                  },
                  "createdAt": "2023-07-13T19:21:29.798063+00:00"
                }
              ],
              "entityType": "PackageLicense",
              "enabled": true,
              "createdAt": "2023-07-13T19:21:29.988802+00:00"
            }

        """
        result = None
        url = "/management-of-risk/package-licenses/entity-profile/search"
        data = json.dumps(
            {
                "packageId": package_id,
                "licenseName": license_name,
                "projectId": project_id,
                "actionType": action_type,
                "to": to_when
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == OK:
            result = response.json()
        return result

    def create_sbom_report(
            self, scan_id: str, file_format: str, hide_dev_and_test_dependencies: bool = False,
            show_only_effective_licenses: bool = False
    ) -> str:
        """

        Args:
            scan_id (str):
            file_format (str): CycloneDxJson, CycloneDxXml or SpdxJson
            hide_dev_and_test_dependencies (bool): If you would like to exclude all development and test dependencies
                        from the SBOM, set this flag as true.
            show_only_effective_licenses (bool): If you would like to exclude all licenses that aren't marked as
                        "Effective" from the SBOM, set this flag as true.

        Returns:
            exportId (str)
        """
        result = None
        if file_format not in ["CycloneDxJson", "CycloneDxXml", "SpdxJson"]:
            raise ValueError("file_format should be CycloneDxJson, CycloneDxXml or SpdxJson")
        url = "/export/requests?"
        options = []
        if hide_dev_and_test_dependencies:
            options.append("hideDevAndTestDependencies=True")
        if show_only_effective_licenses:
            options.append("showOnlyEffectiveLicenses=True")
        url += "&".join(options)
        data = json.dumps(
            {
                "ScanId": f"{scan_id}",
                "FileFormat": f"{file_format}"
            }
        )
        response = self.api_client.post_request(relative_url=url, data=data)
        if response.status_code == ACCEPTED:
            result = response.json().get("exportId")
        return result

    def get_sbom_report_creation_status(self, export_id: str) -> dict:
        """

        Args:
            export_id (str): The unique identifier of the report for which you would like to get the status and download
                     link.

        Returns:
            dict
        """
        result = None
        url = f"/export/requests?exportId={export_id}"
        response = self.api_client.get_request(relative_url=url)
        if response.status_code == OK:
            result = response.json()
        return result

    def get_sbom_supported_file_formats(self) -> dict:
        result = None
        url = f"export/file-formats"
        response = self.api_client.get_request(relative_url=url)
        if response.status_code == OK:
            result = response.json()
        return result

    def run_file_analysis(self, file_path_to_analyze: str, analysis_type: str = "sbom") -> str:
        """

        Args:
            file_path_to_analyze (str):
            analysis_type (str):

        Returns:
            str
        """
        request_id = None
        url = f"/analysis/requests/?AnalysisType={analysis_type}"

        file_name = os.path.basename(file_path_to_analyze)
        with open(file_path_to_analyze, "rb") as a_file:
            file_content = a_file.read()
        m = MultipartEncoder(
            fields={
                "fileToAnalyse": (file_name, file_content, "text/plain")
            }
        )
        headers = {"Content-Type": m.content_type}
        response = self.api_client.post_request(relative_url=url, data=m, headers=headers)
        if response.status_code == ACCEPTED:
            request_id = response.json().get("requestId")
        return request_id

    def retrieve_analysis_result(self, request_id: str) -> dict:
        result = None
        url = f"/analysis/requests/{request_id}"
        response = self.api_client.get_request(relative_url=url)
        if response.status_code == OK:
            result = response.json()
        return result

    def get_number_of_vulnerabilities_risks_by_scan_id(
            self, scan_id: str, is_exploitable_path_enabled: bool = False
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):

        Returns:
            example:
            {'vulnerabilitiesRisksByScanId': {'risksLevelCounts': {'critical': 0, 'empty': 0, 'high': 48, 'low': 0,
            'medium': 30, 'none': 0}, 'totalCount': 78}}
        """
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        query = ("query { "
                 "vulnerabilitiesRisksByScanId ("
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled},"
                 f"scanId: \"{scan_id}\","
                 'where: {and:[{and:[{isIgnored:{eq:false}}]}]}'
                 ")"
                 "{ totalCount, risksLevelCounts { critical, high, medium, low, none, empty } }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_supply_chain_risks_by_scan_id(self, scan_id: str) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):

        Returns:
            example:
            {'supplyChainRisksByScanId': {'risksLevelCounts': {'critical': 0, 'empty': 0, 'high': 0, 'low': 0,
             'medium': 0, 'none': 0}, 'totalCount': 0}}
        """
        query = ("query { "
                 "supplyChainRisksByScanId  ("
                 f"scanId: \"{scan_id}\","
                 'where: {and:[{and:[{isIgnore:{eq:false}}]}]}'
                 ")"
                 "{ totalCount, risksLevelCounts { critical, high, medium, low, none, empty } }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_outdated_packages_by_scan_id(self, scan_id: str) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):

        Returns:
            example:
            {"packagesRows":{"totalCount":201}}
        """
        query = ("query { "
                 "packagesRows   ("
                 f"scanId: \"{scan_id}\","
                 'where: {and:[{outdatedModel:{and:[{versionsInBetween:{gte:1}}]}}]}'
                 ")"
                 "{ totalCount }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_legal_risks_by_scan_id(self, scan_id: str) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):

        Returns:
            example:
             {'legalRisksByScanId': {'risksLevelCounts': {'critical': 0, 'empty': 0, 'high': 0, 'low': 47, 'medium': 0,
              'none': 0}, 'totalCount': 47}}
        """
        query = ("query { "
                 "legalRisksByScanId   ("
                 f"scanId: \"{scan_id}\","
                 'where: null'
                 ")"
                 "{  totalCount, risksLevelCounts { critical, high, medium, low, none, empty } }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_vulnerabilities_risks_by_scan_id(
            self, scan_id: str, is_exploitable_path_enabled: bool = False, take: int = 10, skip: int = 0
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):
            take (int):
            skip (int):

        Returns:
            dict
        """
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        query = ("query { "
                 "vulnerabilitiesRisksByScanId ("
                 "where: null, "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 'order: {score: DESC}, '
                 f"scanId:  \"{scan_id}\", "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled})"
                 " { totalCount, undisclosedRiskLevelCounts { empty, critical, high, medium, low, none }, "
                 "items { credit, state, isIgnored, cve, cwe, description, packageId, severity, type, published, "
                 "score, violatedPolicies, isExploitable, isKevDataExists, isExploitDbDataExists, relation, "
                 "epssData { cve, date, epss, percentile }, isEpssDataExists, detectionDate, isVulnerabilityNew, "
                 "cweInfo { title }, packageInfo { name, packageRepository, version }, "
                 "exploitablePath { methodMatch { fullName, line, namespace, shortName, sourceFile }, "
                 "methodSourceCall { fullName, line, namespace, shortName, sourceFile } }, "
                 "vulnerablePackagePath { id, isDevelopment, isResolved, name, version, vulnerabilityRiskLevel }, "
                 "references { comment, type, url }, cvss2 { attackComplexity, attackVector, authentication, "
                 "availability, availabilityRequirement, baseScore, collateralDamagePotential, confidentiality, "
                 "confidentialityRequirement, exploitCodeMaturity, integrityImpact, integrityRequirement, "
                 "remediationLevel, reportConfidence, targetDistribution }, cvss3 { attackComplexity, attackVector,"
                 " availability, availabilityRequirement, baseScore, confidentiality, confidentialityRequirement, "
                 "exploitCodeMaturity, integrity, integrityRequirement, privilegesRequired, remediationLevel, "
                 "reportConfidence, scope, userInteraction }, cvss4 { attackComplexity, attackVector, "
                 "attackRequirements, baseScore, privilegesRequired, userInteraction, vulnerableSystemConfidentiality,"
                 " vulnerableSystemIntegrity, vulnerableSystemAvailability, subsequentSystemConfidentiality, "
                 "subsequentSystemIntegrity, subsequentSystemAvailability }, pendingState, pendingChanges, "
                 "packageState { type, value }, pendingScore, pendingSeverity, isScoreOverridden } } "
                 " }")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_one_vulnerability(self, scan_id: str, vulnerability_id: str, package_id: str) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            vulnerability_id (str):
            package_id (str):

        Returns:
            Response
        """
        query = ("query { "
                 "vulnerability  ("      
                 f"scanId:  \"{scan_id}\", "
                 f"vulnerabilityId:  \"{vulnerability_id}\", "
                 f"packageId:  \"{package_id}\""
                 ")"
                 "{ packageState { type, value }, assignedPolicies, violatedPolicies, pendingChanges, pendingState, "
                 "state, score, pendingScore, pendingSeverity, isScoreOverridden, morEntityProfilesApplied, credit, "
                 "notes, isIgnored, cve, cwe, description, packageId, severity, type, published, isKevDataExists, "
                 "isExploitDbDataExists, isVulnerabilityNew, detectionDate, relation, vulnerabilityFixResolutionText, "
                 "cweInfo { title }, packageInfo { name, packageRepository, version }, isExploitable, exploitablePath "
                 "{ methodMatch { fullName, line, namespace, shortName, sourceFile }, methodSourceCall { fullName, "
                 "line, namespace, shortName, sourceFile } }, "
                 "vulnerablePackagePath { id, isDevelopment, isResolved, "
                 "name, version, vulnerabilityRiskLevel }, "
                 "references { comment, type, url }, "
                 "cvss2 { attackComplexity, attackVector, authentication, availability, availabilityRequirement,"
                 " baseScore, collateralDamagePotential, confidentiality, confidentialityRequirement,"
                 " exploitCodeMaturity, integrityImpact, integrityRequirement, remediationLevel, reportConfidence, "
                 "targetDistribution, severity }, cvss3 { attackComplexity, attackVector, availability,"
                 " availabilityRequirement, baseScore, confidentiality, confidentialityRequirement, "
                 "exploitCodeMaturity, integrity, integrityRequirement, privilegesRequired, remediationLevel, "
                 "reportConfidence, scope, userInteraction, severity }, "
                 "cvss4 { attackComplexity, attackVector, attackRequirements, privilegesRequired, userInteraction, "
                 "vulnerableSystemConfidentiality, vulnerableSystemIntegrity, vulnerableSystemAvailability, "
                 "subsequentSystemConfidentiality, subsequentSystemIntegrity, subsequentSystemAvailability, "
                 "baseScore, severity }, isEpssDataExists, epssData { cve, date, epss, percentile } }"
                 " }")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_supply_chain_risks_by_scan_id(self, scan_id: str, take: int = 10, skip: int = 0) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            take (int):
            skip (int):

        Returns:
            example:
            {'items': [], 'totalCount': 0}
        """
        query = ("query { "
                 "supplyChainRisksByScanId ("
                 "where: null, "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 'order: {score: DESC}, '
                 f"scanId:  \"{scan_id}\""
                 ")"
                 " { totalCount, items { state, description, id, identifiedInPackage, identifiedInPackageName,"
                 " identifiedInPackageVersion, score, severity, title, type, cve, violatedPolicies, relation,"
                 " publishDate, detectionDate, pendingState, pendingChanges, packageState { type, value }, "
                 "pendingScore, pendingSeverity, originalScore } }"
                 " }")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_legal_risks_by_scan_id(self, scan_id: str, take: int = 10, skip: int = 0) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            take (int):
            skip (int):

        Returns:
            example:
            {'items': [], 'totalCount': 0}
        """
        query = ("query { "
                 "legalRisksByScanId  ("
                 "where: null, "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 'order: {score: DESC}, '
                 f"scanId:  \"{scan_id}\""
                 ")"
                 " { totalCount, items { licenseName, packageId, violatedPolicies, packageName, packageVersion, "
                 "relation, score, severity, state, isTest, isDev, message } } "
                 " }")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_direct_third_party_packages_by_scan_id(
            self, scan_id: str, is_exploitable_path_enabled: bool = False, take: int = 10, skip: int = 0,
            is_private_dependency: bool = False
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):
            take (int):
            skip (int):
            is_private_dependency (bool):

        Returns:
            dict
        """
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        private_dependency_operator = "neq"
        if is_private_dependency:
            private_dependency_operator = "eq"
        query = ("query { "
                 "packagesRows ("
                 "where: {relation:{or:[{eq:\"Direct\"},{eq:\"Mixed\"}]},isPrivateDependency:{"
                 f"{private_dependency_operator}:true"
                 "},"
                 "isSaasProvider:{eq:false}}, "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 "order: {risks:DESC}, "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}, "
                 f"scanId: \"{scan_id}\""
                 ")"
                 "{ items { packageId, name, version, isViolatingPolicy, isMalicious, dependencyPathCount, "
                 "violatedPoliciesCount, violatedPolicies, relation, matchType, legalRiskLevel, isDev, "
                 "remediationTaskId, isTest, isNpmVerified, isPluginDependency, isFramework, packageRepository,"
                 " packageUsage, releaseDate, isPrivateDependency, outdatedModel { newestVersion, versionsInBetween, "
                 "newestLibraryDate }, saasProviderInfo { name, key, type }, effectiveLicenses { name, riskLevel },"
                 " risks { vulnerabilities { critical, high, medium, low, none }, legalRisk { critical, high, medium,"
                 " low, none }, supplyChainRisks { critical, high, medium, low, none }, vulnerabilitiesWithoutIgnored {"
                 " critical, high, medium, low, none }, supplyChainRisksWithoutIgnored { critical, high, medium, low,"
                 " none } } }, totalCount } "
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_transitive_third_party_packages_by_scan_id(
            self, scan_id: str, is_exploitable_path_enabled: bool = False, take: int = 10, skip: int = 0,
            is_private_dependency: bool = False
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):
            take (int):
            skip (int):
            is_private_dependency (bool):

        Returns:

        """
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        private_dependency_operator = "neq"
        if is_private_dependency:
            private_dependency_operator = "eq"
        query = ("query { "
                 "packagesRows ("
                 "where: {relation:{or:[{eq:\"Transitive\"},{eq:\"Mixed\"}]},isPrivateDependency:{"
                 f"{private_dependency_operator}:true"
                 "}, "
                 "isSaasProvider:{eq:false}}, "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 "order: {risks:DESC}, "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}, "
                 f"scanId: \"{scan_id}\""
                 ")"
                 "{ items { packageId, name, version, isViolatingPolicy, isMalicious, dependencyPathCount, "
                 "violatedPoliciesCount, violatedPolicies, relation, matchType, legalRiskLevel, isDev, "
                 "remediationTaskId, isTest, isNpmVerified, isPluginDependency, isFramework, packageRepository, "
                 "packageUsage, releaseDate, isPrivateDependency, outdatedModel { newestVersion, versionsInBetween, "
                 "newestLibraryDate }, saasProviderInfo { name, key, type }, effectiveLicenses { name, riskLevel }, "
                 "risks { vulnerabilities { critical, high, medium, low, none }, legalRisk { critical, high, medium, "
                 "low, none }, supplyChainRisks { critical, high, medium, low, none }, vulnerabilitiesWithoutIgnored {"
                 " critical, high, medium, low, none }, supplyChainRisksWithoutIgnored { critical, high, medium, low,"
                 " none } } }, totalCount }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_package_details_by_scan_id_and_package_id(
            self, scan_id: str, package_id: str, is_exploitable_path_enabled: bool = False
    ) -> Response:
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        query = ("query { "
                 "package ("
                 f"packageId: \"{package_id}\", "
                 f"scanId: \"{scan_id}\", "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}"
                 ") "
                 "{ dummyRiskyVersion, isPotentialRiskyPackage, isIgnored, pendingChanges, morEntityProfilesApplied, "
                 "isViolatingPolicy, name, packageId, remediationTaskId, isPrivateDependency, isUnresolved, matchType, "
                 "locations, directDependenciesCount, transitiveDependenciesCount, releaseDate, version, "
                 "packageRepository, isMalicious, isTest, isPluginDependency, isDev, isNpmVerified, isFramework, "
                 "packageCredibility { contributorReputation, packageReliability, runTimeBehavior }, "
                 "dependencyPath { id, name, version, isResolved, isDevelopment, vulnerabilityRiskLevel }, "
                 "licenses { referenceType, reference, packageId, packageName, packageVersion, name, riskLevel, "
                 "copyrightRiskLevel, patentRiskLevel, copyLeftType, riskScore, state }, "
                 "outdatedModel { newestVersion, versionsInBetween, newestLibraryDate }, "
                 "packageUsageModel { "
                 " importsCalled { sourceFile, line, fullName, shortName }, "
                 " methodsCalled { methodSourceCall { sourceFile, line, fullName, shortName } }, "
                 " usageType, packageUsageComplexity }, "
                 "risks { vulnerabilities { critical, high, medium, low, none }, "
                 "legalRisk { critical, high, medium, low, none }, "
                 "supplyChainRisks { critical, high, medium, low, none }, "
                 "vulnerabilitiesWithoutIgnored { critical, high, medium, low, none }, "
                 "supplyChainRisksWithoutIgnored { critical, high, medium, low, none } } }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_packages_by_scan_id(self, scan_id: str, is_exploitable_path_enabled: bool = False) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):

        Returns:
            example:
            {'packagesRows': {'totalCount': 245, 'totalDevCount': 70, 'totalDevOrTestCount': 70}}
        """
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        query = ("query { "
                 "packagesRows ("
                 f"scanId: \"{scan_id}\", "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}, "
                 "where: {}) { totalCount, totalDevCount, totalDevOrTestCount } "
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_direct_third_party_packages_by_scan_id(
            self, scan_id: str, is_exploitable_path_enabled: bool = False, is_private_dependency: bool = False
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):
            is_private_dependency (bool):

        Returns:
            example:
            {'packagesRows': {'hasMaliciousPackage': False, 'maxVulnerabilitiesCount': 36, 'totalCount': 44,
            'totalDevCount': 70, 'totalDevOrTestCount': 70, 'totalPolicyViolationsCount': 0}}
        """
        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        private_dependency_operator = "neq"
        if is_private_dependency:
            private_dependency_operator = "eq"
        query = ("query { "
                 "packagesRows ("
                 f"scanId: \"{scan_id}\", "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}, "
                 "where: {relation:{or:[{eq:\"Direct\"},{eq:\"Mixed\"}]},"
                 "isPrivateDependency:{"
                 f"{private_dependency_operator}"
                 ":true},isSaasProvider:{eq:false}}"
                 ")"
                 "{ totalCount, totalDevCount, totalPolicyViolationsCount, maxVulnerabilitiesCount, "
                 "hasMaliciousPackage, totalDevOrTestCount}"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_transitive_third_party_packages_by_scan_id(
            self, scan_id: str, is_exploitable_path_enabled: bool = False, is_private_dependency: bool = False
    ) -> Response:
        """
        This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):
            is_private_dependency (bool):

        Returns:
            example:
            {'packagesRows': {'hasMaliciousPackage': False, 'maxVulnerabilitiesCount': 36, 'totalCount': 206,
            'totalDevCount': 70, 'totalDevOrTestCount': 70, 'totalPolicyViolationsCount': 0}}
        """

        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        private_dependency_operator = "neq"
        if is_private_dependency:
            private_dependency_operator = "eq"
        query = ("query { "
                 "packagesRows ("
                 f"scanId: \"{scan_id}\", "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}, "
                 "where: {relation:{or:[{eq:\"Transitive\"},{eq:\"Mixed\"}]},isPrivateDependency:{"
                 f"{private_dependency_operator}"
                 ":true},"
                 "isSaasProvider:{eq:false}}"
                 ")"
                 " { totalCount, totalDevCount, totalPolicyViolationsCount, maxVulnerabilitiesCount, "
                 "hasMaliciousPackage, totalDevOrTestCount } "
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_number_of_packages_used_for_accessing_saas_services(
            self, scan_id: str, is_exploitable_path_enabled: bool = False
    ) -> Response:
        """
        This is a GraphQL API
        Args:
            scan_id (str):
            is_exploitable_path_enabled (bool):

        Returns:
            Response
        """

        is_exploitable_path_enabled = "true" if is_exploitable_path_enabled else "false"
        query = ("query { "
                 "packagesRows ("
                 f"scanId: \"{scan_id}\", "
                 f"isExploitablePathEnabled: {is_exploitable_path_enabled}, "
                 "where: {isSaasProvider:{eq:true}}"
                 ")"
                 " { totalCount, totalDevCount, totalPolicyViolationsCount, maxVulnerabilitiesCount, "
                 "hasMaliciousPackage, totalDevOrTestCount } "
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_container_packages_by_scan_id(
            self, scan_id: str, fetch_runtime_data: bool = False, take: int = 10, skip: int = 0
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            fetch_runtime_data (bool):
            take (int):
            skip (int):

        Returns:
            example:
                {'containerPackages': {'items': [], 'totalCount': 0}}
        """
        fetch_runtime_data = "true" if fetch_runtime_data else "false"
        query = ("query { "
                 "containerPackages  ("
                 f"scanId: \"{scan_id}\", "
                 f"fetchRuntimeData: {fetch_runtime_data}, "
                 f"take: {take}, " 
                 f"skip: {skip}, "
                 "where: null, "
                 'order: {isMalicious:DESC,runtimeUsage:DESC,vulnerabilitiesCounter:{high:DESC}}'
                 ")"
                 "{ totalCount, items { packageName, packageVersion, imageName, imageTag, identifiedBy, deploymentType,"
                 "runtimeUsage, imageOrigins, isMalicious, vulnerabilitiesCounter { high, medium, low } } }  "
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_container_vulnerabilities_by_scan_id(
            self, scan_id: str, fetch_runtime_data: bool = False, take: int = 10, skip: int = 0
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            fetch_runtime_data (bool):
            take (int):
            skip (int):

        Returns:
            example:
                {"containerVulnerabilities":{"totalCount":0,"items":[]}}
        """
        fetch_runtime_data = "true" if fetch_runtime_data else "false"
        query = ("query { "
                 "containerVulnerabilities  ("
                 f"scanId: \"{scan_id}\", "
                 f"fetchRuntimeData: {fetch_runtime_data}, "
                 f"take: {take}, " 
                 f"skip: {skip}, "
                 "where: null, "
                 'order: {riskFactors:{isMalicious:DESC},severity:DESC}'
                 ")"
                 "{totalCount, items {cve, cwe, name, version, published, severity, riskFactors {isMalicious, isUsed}}}"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_package_licenses_by_scan_id(self, scan_id: str, take: int = 10, skip: int = 0) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            take (int):
            skip (int):

        Returns:

        """
        query = ("query { "
                 "packageLicensesByScanId   ("
                 f"scanId: \"{scan_id}\", "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 "where: null, "
                 'order: {pendingState:ASC,riskScore:DESC}'
                 ")"
                 "{totalCount, items { copyLeftType, copyrightRiskLevel, isViolatingPolicy, licenseUrl, name, "
                 "patentRiskLevel, reference, referenceType, licenseSourcePath, relation, riskLevel, riskScore, "
                 "violatedPolicies, violatedPoliciesCount, state, pendingChanges, pendingState, isForbidden, status, "
                 "package { link, numberOfLicensesInPackage, packageId, packageName, packageVersion }, "
                 "packageState { type, value } } }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_down_stream_remediation_by_scan_id(
            self, scan_id: str, include_broken_methods: bool = True, take: int = 10, skip: int = 0
    ) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):
            include_broken_methods (bool):
            take (int):
            skip (int):

        Returns:
            example:
                {'downstreamRemediation': {'items': [], 'totalCount': 0}}
        """
        include_broken_methods = "true" if include_broken_methods else "false"
        query = ("query { "
                 "downstreamRemediation    ("
                 f"scanId: \"{scan_id}\", "
                 f"includeBrokenMethods: {include_broken_methods}, "
                 f"take: {take}, "
                 f"skip: {skip}, "
                 "where: null, "
                 'order: {summaryQuery:{packageId:ASC}}'
                 ")"
                 "{totalCount, items { id, summaryQuery { effortEstimation, packageName, packageVersion, packageId, "
                 "criticalVulnerabilityCount, highVulnerabilityCount, mediumVulnerabilityCount, lowVulnerabilityCount,"
                 "effortEstimation, impact, hasExploitablePath, packages { name, version, criticalVulnerabilityCount,"
                 " highVulnerabilityCount, mediumVulnerabilityCount, lowVulnerabilityCount, parent { name, version}}}}}"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_scan_info_by_scan_id(self, scan_id: str) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):

        Returns:
            example:
            {
                "scanInfo": {
                    "hasWarnings": false,
                    "totalManifestsCount": 1,
                    "totalPackagesCount": 245,
                    "identifiedBy": [
                        {
                            "matchType": "Filename",
                            "count": 240
                        },
                        {
                            "matchType": "Sha1",
                            "count": 5
                        }
                    ],
                    "manifests": [
                        {
                            "dependenciesCount": 309,
                            "dependencyResolverStatus": "FullResults",
                            "manifestPath": "pom.xml",
                            "message": "",
                            "resolvingModuleType": "Maven"
                        }
                    ],
                    "deltaScan": false
                }
            }
        """
        query = ("query { "
                 "scanInfo     ("
                 f"scanId: \"{scan_id}\" "
                 ")"
                 "{hasWarnings, totalManifestsCount, totalPackagesCount, identifiedBy { matchType, count }, "
                 "manifests { dependenciesCount, dependencyResolverStatus, manifestPath, message, resolvingModuleType},"
                 "deltaScan }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response

    def get_scan_progress_by_scan_id(self, scan_id: str) -> Response:
        """
            This is a GraphQL API
        Args:
            scan_id (str):

        Returns:
            example:
                {'scanProgress': {'totalDuration': 35847.367, 'data': [
        {'name': 'Generating download link', 'startTime': '2024-11-22T01:54:01.129Z', 'duration': 0.253,
        'status': 'Done'},
        {'name': 'Download Project Code', 'startTime': '2024-11-22T01:54:01.145Z', 'duration': 69.031,
        'status': 'Done'},
        {'name': 'CollectEvidencesScanPipelineStep', 'startTime': '2024-11-22T01:54:01.227Z', 'duration': 0.001,
        'status': 'Done'},
         {'name': 'Collecting Evidence', 'startTime': '2024-11-22T01:54:01.237Z', 'duration': 5241.963,
         'status': 'Done'},
          {'name': 'Store Ignored Vulnerabilities in Scan Results', 'startTime': '2024-11-22T01:54:06.547Z',
          'duration': 7.692, 'status': 'Done'},
          {'name': 'Generate Risk Report', 'startTime': '2024-11-22T01:54:06.565Z', 'duration': 15284.921,
          'status': 'Done'},
          {'name': 'Find Private Packages', 'startTime': '2024-11-22T01:54:36.900Z', 'duration': 0.815,
          'status': 'Done'},
          {'name': 'Global Inventory Publisher', 'startTime': '2024-11-22T01:54:36.918Z', 'duration': 0.769,
          'status': 'Done'},
          {'name': 'Correlating container vulnerabilities', 'startTime': '2024-11-22T01:54:06.498Z',
          'duration': 27.277, 'status': 'Done'},
          {'name': 'Handle Container Evidences', 'startTime': '2024-11-22T01:54:06.490Z', 'duration': 47.252,
          'status': 'Done'},
          {'name': 'Generate Risk Management Report', 'startTime': '2024-11-22T01:54:21.862Z', 'duration': 0.777,
          'status': 'Done'},
           {'name': 'Fetch Generate Risk Management Report Result', 'startTime': '2024-11-22T01:54:36.888Z',
           'duration': 0.958, 'status': 'Done'}
        ]}}
        """
        query = ("query { "
                 "scanProgress  ("
                 f"scanId: \"{scan_id}\" "
                 ")"
                 "{ totalDuration, data { name, startTime, duration, status } }"
                 "}")
        response = self.api_client.get_request(relative_url=self.gql_relative_url, params={"query": query})
        return response


def get_all_projects(project_name=None):
    return Sca().get_all_projects(project_name=project_name)


def check_if_project_already_exists(project_name=None):
    return Sca().check_if_project_already_exists(project_name=project_name)


def create_a_new_project(project_name, assigned_teams=None):
    return Sca().create_a_new_project(project_name=project_name, assigned_teams=assigned_teams)


def get_project_id_by_name(project_name):
    return Sca().get_project_id_by_name(project_name=project_name)


def get_project_by_id(project_id):
    return Sca().get_project_by_id(project_id=project_id)


def update_project(project_id, project_name=None, assigned_teams=None):
    return Sca().update_project(project_id=project_id, project_name=project_name, assigned_teams=assigned_teams)


def delete_project(project_id):
    return Sca().delete_project(project_id=project_id)


def get_all_scans_associated_with_a_project(project_id):
    return Sca().get_all_scans_associated_with_a_project(project_id=project_id)


def get_latest_scan_id_of_a_project(project_id):
    return Sca().get_latest_scan_id_of_a_project(project_id=project_id)


def get_scan_by_id(scan_id):
    return Sca().get_scan_by_id(scan_id=scan_id)


def get_scan_status(scan_id):
    return Sca().get_scan_status(scan_id=scan_id)


def get_scan_settings(scan_id):
    return Sca().get_scan_settings(scan_id=scan_id)


def get_risk_report_summary(project_id=None, size=10, skip=0):
    return Sca().get_risk_report_summary(project_id=project_id, size=size, skip=skip)


def get_packages_of_a_scan(scan_id):
    return Sca().get_packages_of_a_scan(scan_id=scan_id)


def get_vulnerabilities_of_a_scan(scan_id):
    return Sca().get_vulnerabilities_of_a_scan(scan_id=scan_id)


def get_licenses_of_a_scan(scan_id):
    return Sca().get_licenses_of_a_scan(scan_id=scan_id)


def get_warnings_of_a_scan(scan_id):
    return Sca().get_warnings_of_a_scan(scan_id=scan_id)


def ignore_a_vulnerability_for_a_specific_package_and_project(project_id, vulnerability_id, package_id):
    return Sca().ignore_a_vulnerability_for_a_specific_package_and_project(
        project_id=project_id, vulnerability_id=vulnerability_id, package_id=package_id
    )


def undo_the_ignore_state_of_an_ignored_vulnerability(project_id, vulnerability_id, package_id):
    return Sca().undo_the_ignore_state_of_an_ignored_vulnerability(
        project_id=project_id, vulnerability_id=vulnerability_id, package_id=package_id
    )


def get_settings_for_a_specific_project(project_id):
    return Sca().get_settings_for_a_specific_project(project_id=project_id)


def update_settings_for_a_specific_project(project_id, enable_exploitable_path):
    return Sca().update_settings_for_a_specific_project(project_id=project_id,
                                                        enable_exploitable_path=enable_exploitable_path)


def generate_upload_link_for_scanning(project_id):
    return Sca().generate_upload_link_for_scanning(project_id=project_id)


def upload_zip_content_for_scanning(upload_link, zip_file_path):
    return Sca().upload_zip_content_for_scanning(upload_link=upload_link, zip_file_path=zip_file_path)


def scan_previously_uploaded_zip(project_id, uploaded_file_url):
    return Sca().scan_previously_uploaded_zip(project_id=project_id, uploaded_file_url=uploaded_file_url)


def generate_upload_link():
    return Sca().generate_upload_link()


def upload_zip_file(upload_link, zip_file_path):
    return Sca().upload_zip_file(upload_link=upload_link, zip_file_path=zip_file_path)


def scan_zip_file_or_github_file(project_id, project_type, handler_url):
    return Sca().scan_zip_file_or_github_file(project_id=project_id, project_type=project_type, handler_url=handler_url)


def get_comments_associated_with_a_project(project_id):
    return Sca().get_comments_associated_with_a_project(project_id=project_id)


def comment_a_vulnerability_for_a_specific_package_and_project(project_id, vulnerability_id, package_id, comment):
    return Sca().comment_a_vulnerability_for_a_specific_package_and_project(
        project_id=project_id, vulnerability_id=vulnerability_id, package_id=package_id, comment=comment
    )


def get_states_associated_with_a_project(project_id):
    return Sca().get_states_associated_with_a_project(project_id=project_id)


def change_state_of_a_vulnerability_for_a_specific_package_and_project(project_id, vulnerability_id, package_id, state):
    return Sca().change_state_of_a_vulnerability_for_a_specific_package_and_project(
        project_id=project_id, vulnerability_id=vulnerability_id, package_id=package_id, state=state
    )


def get_scan_reports(scan_id, report_format="Json", data_types=("All",)):
    return Sca().get_scan_reports(scan_id=scan_id, report_format=report_format, data_types=data_types)


def get_aggregated_risks(package_type, package_name, version):
    return Sca().get_aggregated_risks(package_type=package_type, package_name=package_name, version=version)


def get_artifact_license(package_type, package_name, version):
    return Sca().get_artifact_license(package_type=package_type, package_name=package_name, version=version)


def get_artifact_info(package_type, package_name, version):
    return Sca().get_artifact_info(package_type=package_type, package_name=package_name, version=version)


def get_suggest_private_package(package_type, package_name, version):
    return Sca().get_suggest_private_package(package_type=package_type, package_name=package_name, version=version)


def execute_action_on_package_vulnerabilities(package_name, package_manager, vulnerability_id, package_version,
                                              project_ids, actions):
    return Sca().execute_action_on_package_vulnerabilities(
        package_name, package_manager, vulnerability_id, package_version, project_ids, actions
    )


def evaluate_package_vulnerabilities(scan_id, entities):
    return Sca().evaluate_package_vulnerabilities(scan_id, entities)


def disable_an_action_of_package_vulnerability(package_name, package_version, package_manager, vulnerability_id,
                                               project_ids, action_type):
    return Sca().disable_an_action_of_package_vulnerability(
        package_name, package_version, package_manager, vulnerability_id, project_ids, action_type
    )


def get_changes_of_package_vulnerabilities_of_a_project(project_id, from_when, skip, take):
    return Sca().get_changes_of_package_vulnerabilities_of_a_project(project_id, from_when, skip, take)


def search_entity_profile_of_package_vulnerabilities(package_name, package_version, package_manager, vulnerability_id,
                                                     project_id, action_type, to_when):
    return Sca().search_entity_profile_of_package_vulnerabilities(
        package_name, package_version, package_manager, vulnerability_id, project_id, action_type, to_when
    )


def execute_actions_on_supply_chain_risks(package_name, package_manager, supply_chain_risk_id, package_version,
                                          project_ids, actions):
    return Sca().execute_actions_on_supply_chain_risks(
        package_name, package_manager, supply_chain_risk_id, package_version, project_ids, actions
    )


def evaluate_supply_chain_risks(scan_id, entities):
    return Sca().evaluate_supply_chain_risks(scan_id, entities)


def disable_an_action_for_a_supply_chain_risk(package_name, package_version, package_manager, supply_chain_risk_id,
                                              project_ids, action_type):
    return Sca().disable_an_action_for_a_supply_chain_risk(
        package_name, package_version, package_manager, supply_chain_risk_id, project_ids, action_type
    )


def get_changes_of_supply_chain_risk(project_id, from_when, skip, take):
    return Sca().get_changes_of_supply_chain_risk(project_id, from_when, skip, take)


def search_entity_profile_of_package_supply_chain_risks(package_name, package_version, package_manager,
                                                        supply_chain_risk_id, project_id, action_type, to_when):
    return Sca().search_entity_profile_of_package_supply_chain_risks(
        package_name, package_version, package_manager, supply_chain_risk_id, project_id, action_type, to_when
    )


def execute_actions_on_package_license(package_id, license_name, project_ids, actions):
    return Sca().execute_actions_on_package_license(package_id, license_name, project_ids, actions)


def evaluate_package_licenses(entities, scan_id):
    return Sca().evaluate_package_licenses(entities, scan_id)


def search_entity_profiles_of_package_licenses(package_id, license_name, project_id, action_type, to_when):
    return Sca().search_entity_profiles_of_package_licenses(package_id, license_name, project_id, action_type, to_when)


def create_sbom_report(scan_id, file_format, hide_dev_and_test_dependencies=False, show_only_effective_licenses=False):
    return Sca().create_sbom_report(scan_id, file_format,
                                    hide_dev_and_test_dependencies=hide_dev_and_test_dependencies,
                                    show_only_effective_licenses=show_only_effective_licenses)


def get_sbom_report_creation_status(export_id):
    return Sca().get_sbom_report_creation_status(export_id=export_id)


def get_sbom_supported_file_formats():
    return Sca().get_sbom_supported_file_formats()


def run_file_analysis(file_path_to_analyze, analysis_type="sbom"):
    return Sca().run_file_analysis(file_path_to_analyze=file_path_to_analyze, analysis_type=analysis_type)


def retrieve_analysis_result(request_id):
    return Sca().retrieve_analysis_result(request_id=request_id)


def get_number_of_vulnerabilities_risks_by_scan_id(scan_id, is_exploitable_path_enabled=False):
    return Sca().get_number_of_vulnerabilities_risks_by_scan_id(scan_id=scan_id,
                                                                is_exploitable_path_enabled=is_exploitable_path_enabled)


def get_number_of_supply_chain_risks_by_scan_id(scan_id):
    return Sca().get_number_of_supply_chain_risks_by_scan_id(scan_id=scan_id)


def get_number_of_outdated_packages_by_scan_id(scan_id):
    return Sca().get_number_of_outdated_packages_by_scan_id(scan_id=scan_id)


def get_number_of_legal_risks_by_scan_id(scan_id):
    return Sca().get_number_of_legal_risks_by_scan_id(scan_id=scan_id)


def get_vulnerabilities_risks_by_scan_id(scan_id, is_exploitable_path_enabled=False, take=10, skip=0):
    return Sca().get_vulnerabilities_risks_by_scan_id(scan_id, is_exploitable_path_enabled=is_exploitable_path_enabled,
                                                      take=take, skip=skip)


def get_one_vulnerability(scan_id, vulnerability_id, package_id):
    return Sca().get_one_vulnerability(scan_id=scan_id, vulnerability_id=vulnerability_id, package_id=package_id)


def get_supply_chain_risks_by_scan_id(scan_id, take=10, skip=0):
    return Sca().get_supply_chain_risks_by_scan_id(scan_id, take=take, skip=skip)


def get_legal_risks_by_scan_id(scan_id, take=10, skip=0):
    return Sca().get_legal_risks_by_scan_id(scan_id, take=take, skip=skip)


def get_direct_third_party_packages_by_scan_id(scan_id, is_exploitable_path_enabled=False, take=10, skip=0):
    return Sca().get_direct_third_party_packages_by_scan_id(scan_id,
                                                            is_exploitable_path_enabled=is_exploitable_path_enabled,
                                                            take=take, skip=skip)


def get_transitive_third_party_packages_by_scan_id(scan_id, is_exploitable_path_enabled=False, take=10, skip=0):
    return Sca().get_transitive_third_party_packages_by_scan_id(scan_id,
                                                                is_exploitable_path_enabled=is_exploitable_path_enabled,
                                                                take=take, skip=skip)


def get_number_of_packages_by_scan_id(scan_id, is_exploitable_path_enabled=False):
    return Sca().get_number_of_packages_by_scan_id(scan_id, is_exploitable_path_enabled=is_exploitable_path_enabled)


def get_number_of_direct_third_party_packages_by_scan_id(scan_id, is_exploitable_path_enabled=False):
    return Sca().get_number_of_direct_third_party_packages_by_scan_id(
        scan_id, is_exploitable_path_enabled=is_exploitable_path_enabled
    )


def get_number_of_transitive_third_party_packages_by_scan_id(scan_id, is_exploitable_path_enabled=False):
    return Sca().get_number_of_transitive_third_party_packages_by_scan_id(
        scan_id, is_exploitable_path_enabled=is_exploitable_path_enabled
    )


def get_number_of_packages_used_for_accessing_saas_services(scan_id, is_exploitable_path_enabled=False):
    return Sca().get_number_of_packages_used_for_accessing_saas_services(
        scan_id, is_exploitable_path_enabled=is_exploitable_path_enabled
    )


def get_container_packages_by_scan_id(scan_id, fetch_runtime_data=False, take=10, skip=0):
    return Sca().get_container_packages_by_scan_id(scan_id, fetch_runtime_data=fetch_runtime_data, take=take, skip=skip)


def get_container_vulnerabilities_by_scan_id(scan_id, fetch_runtime_data=False, take=10, skip=0):
    return Sca().get_container_vulnerabilities_by_scan_id(scan_id, fetch_runtime_data=fetch_runtime_data, take=take,
                                                          skip=skip)


def get_package_licenses_by_scan_id(scan_id, take=0, skip=0):
    return Sca().get_package_licenses_by_scan_id(scan_id, take=take, skip=skip)


def get_down_stream_remediation_by_scan_id(scan_id, include_broken_methods=True, take=10, skip=0):
    return Sca().get_down_stream_remediation_by_scan_id(scan_id, include_broken_methods=include_broken_methods,
                                                        take=take, skip=skip)


def get_scan_info_by_scan_id(scan_id):
    return Sca().get_scan_info_by_scan_id(scan_id)


def get_scan_progress_by_scan_id(scan_id):
    return Sca().get_scan_progress_by_scan_id(scan_id)
