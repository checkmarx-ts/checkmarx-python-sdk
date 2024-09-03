# encoding: utf-8
import json

from .httpRequests import get_request, post_request, patch_request, delete_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK, CREATED, NO_CONTENT, ACCEPTED
from .sast.general.dto import CxServerLicenseData, CxSupportedLanguage, CxTranslationInput, CxUserPersistence


class GeneralAPI:
    """
    CxSAST general API
    """

    @staticmethod
    def get_server_license_data(api_version="4.0"):
        """
        Returns the CxSAST server's license data
        """
        result = None
        relative_url = "/cxrestapi/serverLicenseData"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            json = response.json()
            result = CxServerLicenseData(
                current_audit_users=json["currentAuditUsers"],
                current_projects_count=json["currentProjectsCount"],
                current_users=json["currentUsers"],
                edition=json["edition"],
                expiration_date=json["expirationDate"],
                hid=json["hid"],
                is_osa_enabled=json["isOsaEnabled"],
                max_audit_users=json["maxAuditUsers"],
                max_concurrent_scans=json["maxConcurrentScans"],
                max_loc=json["maxLOC"],
                max_users=json["maxUsers"],
                osa_expiration_date=json["osaExpirationDate"],
                projects_allowed=json["projectsAllowed"],
                supported_languages=[
                    CxSupportedLanguage(
                        is_supported=item["isSupported"],
                        language=item["language"])
                    for item in json["supportedLanguages"]
                ]
            )
        return result

    @staticmethod
    def get_server_system_version(api_version="1.1"):
        """
        Returns version, hotfix number and engine pack version
        Returns:
            {
              "version": "string",
              "hotFix": "string",
              "enginePackVersion": "string"
            }
        """
        result = None
        relative_url = "/cxrestapi/system/version"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def get_result_states(api_version="4.0"):
        """

        Args:
            api_version:

        Returns:

        """
        """
        [
          {
            "id": 0,
            "names": [
              {
                "languageId": 1028,
                "name": "校驗",
                "isConstant": true
              },
              {
                "languageId": 1033,
                "name": "To Verify",
                "isConstant": true
              },
              {
                "languageId": 1034,
                "name": "Para verificar",
                "isConstant": true
              },
              {
                "languageId": 1036,
                "name": "Pour vérifier",
                "isConstant": true
              },
              {
                "languageId": 1041,
                "name": "確認必要",
                "isConstant": true
              },
              {
                "languageId": 1042,
                "name": "확인하려면",
                "isConstant": true
              },
              {
                "languageId": 1046,
                "name": "Verificar",
                "isConstant": true
              },
              {
                "languageId": 1049,
                "name": "Проверять",
                "isConstant": true
              },
              {
                "languageId": 2052,
                "name": "等待确认",
                "isConstant": true
              }
            ],
            "permission": "set-result-state-toverify"
          },
          {
            "id": 1,
            "names": [
              {
                "languageId": 1028,
                "name": "不可利用",
                "isConstant": true
              },
              {
                "languageId": 1033,
                "name": "Not Exploitable",
                "isConstant": true
              },
              {
                "languageId": 1034,
                "name": "No explotable",
                "isConstant": true
              },
              {
                "languageId": 1036,
                "name": "Non exploitable",
                "isConstant": true
              },
              {
                "languageId": 1041,
                "name": "悪用はできない",
                "isConstant": true
              },
              {
                "languageId": 1042,
                "name": "악용할 수 없음",
                "isConstant": true
              },
              {
                "languageId": 1046,
                "name": "Não Exploitável",
                "isConstant": true
              },
              {
                "languageId": 1049,
                "name": "Не эксплуатируемый",
                "isConstant": true
              },
              {
                "languageId": 2052,
                "name": "不可利用",
                "isConstant": true
              }
            ],
            "permission": "set-result-state-notexploitable"
          },
          {
            "id": 2,
            "names": [
              {
                "languageId": 1028,
                "name": "確認",
                "isConstant": false
              },
              {
                "languageId": 1033,
                "name": "Confirmed",
                "isConstant": false
              },
              {
                "languageId": 1034,
                "name": "Confirmado",
                "isConstant": false
              },
              {
                "languageId": 1036,
                "name": "Confirmé",
                "isConstant": false
              },
              {
                "languageId": 1041,
                "name": "確認済み",
                "isConstant": false
              },
              {
                "languageId": 1042,
                "name": "확인됨",
                "isConstant": false
              },
              {
                "languageId": 1046,
                "name": "Confirmado",
                "isConstant": false
              },
              {
                "languageId": 1049,
                "name": "Подтвердил",
                "isConstant": false
              },
              {
                "languageId": 2052,
                "name": "已确认",
                "isConstant": false
              }
            ],
            "permission": "set-result-state-confirmed"
          },
          {
            "id": 3,
            "names": [
              {
                "languageId": 1028,
                "name": "緊急",
                "isConstant": false
              },
              {
                "languageId": 1033,
                "name": "Urgent",
                "isConstant": false
              },
              {
                "languageId": 1034,
                "name": "Urgente",
                "isConstant": false
              },
              {
                "languageId": 1036,
                "name": "Urgent",
                "isConstant": false
              },
              {
                "languageId": 1041,
                "name": "緊急",
                "isConstant": false
              },
              {
                "languageId": 1042,
                "name": "긴급",
                "isConstant": false
              },
              {
                "languageId": 1046,
                "name": "Urgente",
                "isConstant": false
              },
              {
                "languageId": 1049,
                "name": "Срочный",
                "isConstant": false
              },
              {
                "languageId": 2052,
                "name": "紧急",
                "isConstant": false
              }
            ],
            "permission": "set-result-state-urgent"
          },
          {
            "id": 4,
            "names": [
              {
                "languageId": 1028,
                "name": "推薦不可用",
                "isConstant": true
              },
              {
                "languageId": 1033,
                "name": "Proposed Not Exploitable",
                "isConstant": true
              },
              {
                "languageId": 1034,
                "name": "Propuesto no explotable",
                "isConstant": true
              },
              {
                "languageId": 1036,
                "name": "Proposition non exploitable",
                "isConstant": true
              },
              {
                "languageId": 1041,
                "name": "悪用不可を提案",
                "isConstant": true
              },
              {
                "languageId": 1042,
                "name": "수용 할 수 없는 제안",
                "isConstant": true
              },
              {
                "languageId": 1046,
                "name": "Proposta Não Exploitável",
                "isConstant": true
              },
              {
                "languageId": 1049,
                "name": "Предлагается не использовать",
                "isConstant": true
              },
              {
                "languageId": 2052,
                "name": "提议不可利用",
                "isConstant": true
              }
            ],
            "permission": "set-result-state-proposednotexploitable"
          }
        ]
"""
        result = None
        relative_url = "/cxrestapi/sast/resultStates"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def create_result_state(translation_inputs, permission, api_version="4.0"):
        """

        Args:
            translation_inputs (List of `CxTranslationInput`):
            permission (str): example, "set-result-state-toverify"
            api_version (str):

        Returns:
            Id of result state(int)
        """
        result = None
        if translation_inputs and not isinstance(translation_inputs, (list, tuple)):
            raise ValueError("translation_inputs should be list or tuple")
        for item in translation_inputs:
            if item and not isinstance(item, CxTranslationInput):
                raise ValueError("member of translation_inputs should be CxTranslationInput")

        result = None
        post_data = json.dumps(
            {
                "names": [item.to_dict() for item in translation_inputs],
                "permission": permission
            }
        )
        relative_url = "/cxrestapi/sast/resultStates"
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json().get("id")
        return result

    @staticmethod
    def update_result_state(state_id, translation_inputs, permission, api_version="4.0"):
        """

        Args:
            state_id (int):
            translation_inputs (List of `CxTranslationInput`):
            permission (str): example, "set-result-state-toverify"
            api_version (str):

        Returns:
            bool
        """
        is_successful = False
        if translation_inputs and not isinstance(translation_inputs, (list, tuple)):
            raise ValueError("translation_inputs should be list or tuple")
        for item in translation_inputs:
            if item and not isinstance(item, CxTranslationInput):
                raise ValueError("member of translation_inputs should be CxTranslationInput")
        patch_data = json.dumps(
            {
                "names": [item.to_dict() for item in translation_inputs],
                "permission": permission
            }
        )
        relative_url = "/cxrestapi/sast/resultStates/{id}".format(id=state_id)
        response = patch_request(relative_url=relative_url, data=patch_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            is_successful = True
        return is_successful

    @staticmethod
    def delete_result_state(state_id, api_version="4.0"):
        """

        Args:
            state_id (int): The Id of the Result State
            api_version (str):
        Returns:
            bool
        """
        is_successful = False
        relative_url = "/cxrestapi/sast/resultStates/{id}".format(id=state_id)
        response = delete_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == ACCEPTED:
            is_successful = True
        return is_successful

    @staticmethod
    def get_all_scheduled_jobs(api_version="4.0"):
        """

        Args:
            api_version:

        Returns:
            list of dict
            example:
            [{'projectId': 8, 'projectName': 'jvl_git', 'scanDays': ['Sunday'], 'scanTime': '12:00 上午'}]
        """
        result = None
        relative_url = "/cxrestapi/sast/scheduledJobs"
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def get_user_persistence_data_for_current_user(persistence_keys, api_version="5.0"):
        """
        Gets user persistence data for current user
        Args:
            persistence_keys (`list` of `str`): persistence keys
            api_version (str):

        Returns:
            list
        """
        if persistence_keys and not isinstance(persistence_keys, list):
            raise ValueError("parameter persistence_keys should be a list of str")
        for item in persistence_keys:
            if item and not isinstance(item, str):
                raise ValueError("all member in persistence_keys should be a str")
        result = None
        relative_url = "/cxrestapi/userPersistence?"
        relative_url += "&".join(["persistenceKeys={}".format(item) for item in persistence_keys])

        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def update_persistence_data_for_current_user(persistence_items, api_version="5.0"):
        """
        Updates an existing user persistence data for current user
        Args:
            persistence_items (list of `CxUserPersistence`):
            api_version (str):

        Returns:

        """
        is_successful = False
        if persistence_items and not isinstance(persistence_items, list):
            raise ValueError("parameter persistence_items should be a list of CxUserPersistence")
        for item in persistence_items:
            if item and not isinstance(item, CxUserPersistence):
                raise ValueError("member in parameter persistence_items should be CxUserPersistence")
        result = None
        relative_url = "/cxrestapi/userPersistence"
        data = json.dumps(
            [item.to_dict() for item in persistence_items]
        )
        response = patch_request(relative_url=relative_url, data=data, headers=get_headers(api_version))
        if response.status_code == OK:
            is_successful = True
        return is_successful

    @staticmethod
    def get_audit_trail_for_roles(from_date, to_date, api_version="5.0"):
        """

        Args:
            from_date (str):  	From Date (Input Format: yyyy-mm-dd)
            to_date (str):  To Date (Input Format: yyyy-mm-dd)
            api_version (str):

        Returns:
            list of dict
            example:
            [
              {
                'event': 'RoleCreated',
                'id': 1, 'ownerId': -1,
                'ownerName': 'client_credentials_installer',
                'roleDetails': {'id': 0, 'name': None},
                'timeStamp': '2023-08-18T05:14:33.6851454'
              }
            ]
        """
        result = None
        relative_url = "/cxrestapi/sast/roles/auditTrail?fromDate={fromDate}&toDate={toDate}".format(
            fromDate=from_date, toDate=to_date
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def get_audit_trail_for_teams(from_date, to_date, api_version="5.0"):
        """

        Args:
            from_date (str):  	From Date (Input Format: yyyy-mm-dd)
            to_date (str):  To Date (Input Format: yyyy-mm-dd)
            api_version (str):

        Returns:
            list of dict
            example:
                [
                    { 'event': 'TeamCreated',
                      'id': 15769,
                      'ownerId': 1,
                      'ownerName': 'Admin',
                      'teamDetails': None,
                      'timeStamp': '2024-04-15T07:35:45.6458877'
                    }
                ]
        """
        result = None
        relative_url = "/cxrestapi/sast/teams/auditTrail?fromDate={fromDate}&toDate={toDate}".format(
            fromDate=from_date, toDate=to_date
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def get_audit_trail_for_presets(from_date, to_date, api_version="5.0"):
        """

        Args:
            from_date (str):  	From Date (Input Format: yyyy-mm-dd)
            to_date (str):  To Date (Input Format: yyyy-mm-dd)
            api_version (str):

        Returns:
            list of dict
            example:
                [
                    {
                        'event': 'Update',
                        'id': 8,
                        'isSuccessful': True,
                        'ownerId': 1,
                        'ownerName': 'Admin',
                        'presetId': 100002,
                        'presetName': 'Checkmarx Default - Customized',
                        'timeStamp': '2024-01-11T09:44:11.78'
                    }
                ]
        """
        result = None
        relative_url = "/cxrestapi/sast/presets/auditTrail?fromDate={fromDate}&toDate={toDate}".format(
            fromDate=from_date, toDate=to_date
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result

    @staticmethod
    def get_audit_trail_for_results(from_date, to_date, update_type="ALL", api_version="5.0"):
        """

        Args:
            update_type (str): Update Type (ALL, ASSIGN, RESULT_COMMENT, RESULT_SEVERITY, RESULT_STATE) ,
                        default value is "ALL"
            from_date (str):  	From Date (Input Format: yyyy-mm-dd)
            to_date (str):  To Date (Input Format: yyyy-mm-dd)
            api_version (str):

        Returns:
            list of dict
            example:
                [
                    {
                      'id': 48,
                      'isSuccessful': True,
                      'ownerName': 'Admin',
                      'projectId': 5,
                      'scanId': 1000076,
                      'timeStamp': '2024-01-05T11:25:21.943',
                      'updateType': 'RESULT_STATE'
                    }
                ]
        """
        result = None
        if update_type not in ["ALL", "ASSIGN", "RESULT_COMMENT", "RESULT_SEVERITY", "RESULT_STATE"]:
            raise ValueError('parameter update_type should be a member of list '
                             '["ALL", "ASSIGN", "RESULT_COMMENT", "RESULT_SEVERITY", "RESULT_STATE"]')
        relative_url = ("/cxrestapi/sast/results/auditTrail?updateType={updateType}&fromDate={fromDate}"
                        "&toDate={toDate}").format(
            updateType=update_type, fromDate=from_date, toDate=to_date
        )
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = response.json()
        return result
