# encoding: utf-8
"""
    Portal SOAP API
"""
from zeep import Client, Settings

from .config import config_data
from .auth import bear_token

url = config_data.get("base_url") + "/CxWebInterface/Portal/CxWebService.asmx"
wsdl = url + "?wsdl"

settings = Settings(strict=False, force_https=False, extra_http_headers={"Authorization": bear_token})
client = Client(wsdl=wsdl, settings=settings)
client.transport.session.verify = False
factory = client.type_factory("ns0")


def create_new_preset(query_ids, name):
    """

    Args:
        query_ids (`list` of int):
        name (str):

    Returns:
        dict

        sample return:
        {
            'queryIds':  [
                    343
            ],
            'id': 110003,
            'name': 'ddd',
            'owningteam': 1,
            'isPublic': True,
            'owner': None,
            'isUserAllowToUpdate': True,
            'isUserAllowToDelete': True,
            'IsDuplicate': False
        }
    """

    query_ids = factory.ArrayOfLong(query_ids)
    cx_preset_detail = factory.CxPresetDetails(queryIds=query_ids, id=0, name=name, owningteam=1, isPublic=True,
                                               isUserAllowToUpdate=True, isUserAllowToDelete=True, IsDuplicate=False)

    response = client.service.CreateNewPreset(sessionId="0", presrt=cx_preset_detail)
    if not response.IsSuccesfull:
        raise ValueError(response.ErrorMessage)
    p = response.preset
    return {
        'queryIds':  p["queryIds"]["long"],
        'id': p["id"],
        'name': p["name"],
        'owningteam': p["owningteam"],
        'isPublic': p["isPublic"],
        'owner': p["owner"],
        'isUserAllowToUpdate': p["isUserAllowToUpdate"],
        'isUserAllowToDelete': p["isUserAllowToDelete"],
        'IsDuplicate': p["IsDuplicate"]
    }


def delete_preset():
    pass


def delete_project():
    pass


def delete_projects():
    pass
