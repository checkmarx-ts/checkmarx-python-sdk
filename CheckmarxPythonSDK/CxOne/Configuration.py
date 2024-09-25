import json
from CheckmarxPythonSDK.CxOne.httpRequests import get_request

def get_configurations(project_id):    
    relative_url = f"/api/configuration/project?project-id={project_id}"

    response = get_request(relative_url=relative_url)
    return response.json()