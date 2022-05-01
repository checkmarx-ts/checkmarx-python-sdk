# Checkmarx Python SDK

This is wrapper using Python for CxSAST and CxOSA REST API, Portal SOAP API, CxSAST ODATA API, CxSCA REST API. 

By using this SDK, Checkmarx users will be able to do automatic scanning with CxSAST, CxOSA, and CxSCA.

[![Downloads](https://static.pepy.tech/badge/CheckmarxPythonSDK/month)](https://static.pepy.tech/badge/CheckmarxPythonSDK/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/CheckmarxPythonSDK.svg)](https://pypi.org/project/CheckmarxPythonSDK)
[![Contributors](https://img.shields.io/github/contributors/checkmarx-ts/checkmarx-python-sdk.svg)](https://github.com/checkmarx-ts/checkmarx-python-sdk/graphs/contributors)

# Checkmarx API Official Documents

For more information about Checkmarx API, please refer to Checkmarx knowledge Center：

- [CxSAST API Document](https://checkmarx.atlassian.net/wiki/spaces/KC/pages/5767170/CxSAST+API+Guide)  
- [CxOSA API Document](https://checkmarx.atlassian.net/wiki/spaces/CCOD/pages/856653848/CxOSA+API+Guide)
- [Access Control API Document](https://checkmarx.atlassian.net/wiki/spaces/KC/pages/1098645604/Access+Control+REST+API+Summary)
- [CxSCA API Document](https://checkmarx.atlassian.net/wiki/spaces/CD/pages/1782087905/CxSCA+APIs)
- [CxAST API Document](https://checkmarx.atlassian.net/wiki/spaces/AST/pages/3076063341/CxAST+Platform+API+Documentation)
- [CxReporting API Document](https://checkmarx.atlassian.net/wiki/spaces/RS/pages/5860130923/APIs)

# Notice

Please use Python3

# Quick Start

## Install the library

The easiest way to begin using the SDK is to install it using the **pip** command.

```
$ pip install CheckmarxPythonSDK
```

Alternatively, either download and unzip this repository, or clone it to your local drive, and install using the `setup.py` script.

```
$ git clone https://github.com/checkmarx-ts/checkmarx-python-sdk.git
$ python setup.py install
```

Even if you install the SDK using **pip**, you might still want to download or clone this repository for the sample scripts.

## Set up configuration

### Option 1, using config.ini file: 
```buildoutcfg
[checkmarx]
base_url = http://localhost:80
username = ******
password = ******
grant_type = password
scope = sast_rest_api
client_id = resource_owner_client
client_secret = 014DF517-39D1-4453-B7B3-9930C563627C
url =  %(base_url)s/cxrestapi
scan_preset = Checkmarx Default
configuration = Default Configuration
team_full_name = /CxServer
max_try = 3

[CxSCA]
access_control_url = https://platform.checkmarx.net
server = https://api-sca.checkmarx.net
account = ***
username = ***
password = ***

[CxAST]
access_control_url = https://iam.checkmarx.net
server = https://ast.checkmarx.net
tenant_name  = ***
grant_type = refresh_token
client_id = ast-app
client_secret = ***
username = ***
password = ***
refresh_token = ***

[CxReporting]
base_url = http://localhost
reporting_client_url = http://localhost:5001
username = ***
password = ***
grant_type = password
scope = reporting_api
client_id = reporting_service_api
client_secret = 014DF517-39D1-4453-B7B3-9930C563627C
```

configuration file path:

By default, Checkmarx Python SDK looks for `config.ini` or `config.json` file in a `.Checkmarx` folder in your home directory. 
- For windows, it should be like `C:\\Users\\<UserName>\\.Checkmarx\\config.ini`
- For linux and MacOS, it should be like `/home/<UserName>/.Checkmarx/config.ini` 

You can also use `checkmarx_config_path` as environment variable  or command line argument to set up configuration file path.

For CxAST configuration, if you are going to use refresh_token grant type, you must use client id "ast-app", 
refresh_token, ignore client_secret, username, password. If you are going to use client_credentials grant type, 
you must create a client with roles such as ast-scanner, manage-webhook, queries-editor, ast-viewer, manage-application,
manage-project, then fill in your own client_id, client secret, username, password, ignore the refresh_token.

### Option 2, using environment variables or command line arguments

For CxSAST:

    - cxsast_base_url
    - cxsast_username
    - cxsast_password
    - cxsast_grant_type
    - cxsast_scope
    - cxsast_client_id
    - cxsast_client_secret

For CxSCA:

    - cxsca_access_control_url
    - cxsca_server
    - cxsca_account
    - cxsca_username
    - cxsca_password

For CxAST:
    
    - cxast_access_control_url
    - cxast_server
    - cxast_tenant_name
    - cxast_grant_type
    - cxast_client_id
    - cxast_client_secret
    - cxast_username
    - cxast_password
    - cxast_refresh_token
 
 For CxReporting
 
    - cxreporting_base_url
    - cxreporting_reporting_client_url
    - cxreporting_username
    - cxreporting_password
    - cxreporting_grant_type
    - cxreporting_scope
    - cxreporting_client_id
    - cxreporting_client_secret

# Examples
 Please find example scripts from [here](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/examples).


# API List

- [CxAST_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxAST_REST_API_List.md)
- [CxSAST_and_CxOSA_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSAST_and_CxOSA_REST_API_List.md)
- [CxSAST_ODATA_API](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSAST_ODATA_API.md)
- [CxSAST_Portal_SOAP_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSAST_Portal_SOAP_API_List.md)
- [CxSCA_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSCA_REST_API_List.md)
- [CxReporting_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/blob/master/docs/CxReporting_REST_API_List.md)