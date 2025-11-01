# Checkmarx Python SDK

This is wrapper using Python for CxOne, CxSAST and CxOSA REST API, Portal SOAP API, CxSAST ODATA API, CxSCA REST API. 

By using this SDK, Checkmarx users will be able to do automatic scanning with CxOne, CxSAST, CxOSA, and CxSCA.

[![Downloads](https://static.pepy.tech/badge/CheckmarxPythonSDK/month)](https://static.pepy.tech/badge/CheckmarxPythonSDK/month)
[![Supported Versions](https://img.shields.io/pypi/pyversions/CheckmarxPythonSDK.svg)](https://pypi.org/project/CheckmarxPythonSDK)
[![Contributors](https://img.shields.io/github/contributors/checkmarx-ts/checkmarx-python-sdk.svg)](https://github.com/checkmarx-ts/checkmarx-python-sdk/graphs/contributors)

# Checkmarx API Official Documents

For more information about Checkmarx API, please refer to Checkmarx knowledge Center：

- [CxSAST API Document](https://checkmarx.com/resource/documents/en/34965-46552-sast-api-guide.html)  
- [CxOSA API Document](https://checkmarx.com/resource/documents/en/34965-46909-cxosa-api-guide.html)
- [Access Control API Document](https://checkmarx.com/resource/documents/en/34965-46622-access-control--rest--api--v1-5-and-up-.html)
- [CxSCA API Document](https://checkmarx.com/resource/documents/en/34965-19221-checkmarx-sca--rest--api-documentation.html)
- [CxOne API Document](https://checkmarx.com/resource/documents/en/34965-68772-checkmarx-one-api-documentation.html)
- [CxReporting API Document](https://checkmarx.com/resource/documents/en/34965-93162-apis.html)

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
[CxSAST]
base_url = http://localhost:80
username = ******
password = ******
grant_type = password
scope = sast_rest_api
client_id = resource_owner_client
client_secret = 014DF517-39D1-4453-B7B3-9930C563627C


[CxSCA]
access_control_url = https://platform.checkmarx.net
server = https://api-sca.checkmarx.net
account = ***
username = ***
password = ***

[CxOne]
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

For CxOne configuration, if you are going to use refresh_token grant type, you must use client id "ast-app", 
refresh_token, ignore client_secret, username, password. If you are going to use client_credentials grant type, 
you must create a client with roles such as ast-scanner, manage-webhook, queries-editor, ast-viewer, manage-application,
manage-project, then fill in your own client_id, client secret, username, password, ignore the refresh_token.

### Option 2, using environment variables (Upper Case or Lower Case) or command line arguments

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

For CxOne:
    
    - cxone_access_control_url
    - cxone_server
    - cxone_tenant_name
    - cxone_grant_type
    - cxone_client_id
    - cxone_client_secret
    - cxone_username
    - cxone_password
    - cxone_refresh_token
 
 For CxReporting
 
    - cxreporting_base_url
    - cxreporting_reporting_client_url
    - cxreporting_username
    - cxreporting_password
    - cxreporting_grant_type
    - cxreporting_scope
    - cxreporting_client_id
    - cxreporting_client_secret

# Debug Mode
You can use command line option `--cx_debug true` to enable debug mode. In debug mode, it will print out how to load the
configuration file and print every http request send out.

# Configuration Override Sequence

When you run your program with `--cx_debug` command line, it will log the override sequence.

1.	Load default configuration, it will be a python dictionary
2.	Read from ~/.Checkmarx/config.ini, override value by same key
3.	Read from ~/.Checkmarx/config.json, override value by same key
4.	Read from environment variables, override value by same key
5.	Read from command line arguments, override value by same key
6.	You have the final configuration.

# python-dotenv

If you are using python-dotenv, make sure your run `load_dotenv("./<Your-File-Name>.env", override=True)` before import 
any Checkmarx Python SDK function.

# Connect to multiple systems at the same time

Now each API class has been refactored to accept an api_client(class ApiClient) with configuration (class Configuration).
You can pass different api_client with different configuration for each API class.

# CxSAST self-signed certificate
For CxSAST self-signed certificate, you can use the verify in configuration as a string, which is a path to the public 
key of your self-signed certificate. The public key of the self-signed certificate can be exported from browser. Please
export it as a .cert or .pem file.

# Examples
 Please find example scripts from [examples folder](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/examples).


# API List

- [CxOne_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxOne_REST_API_List.md)
- [CxSAST_and_CxOSA_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSAST_and_CxOSA_REST_API_List.md)
- [CxSAST_ODATA_API](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSAST_ODATA_API.md)
- [CxSAST_Portal_SOAP_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSAST_Portal_SOAP_API_List.md)
- [CxSCA_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/tree/master/docs/CxSCA_REST_API_List.md)
- [CxReporting_REST_API_List](https://github.com/checkmarx-ts/checkmarx-python-sdk/blob/master/docs/CxReporting_REST_API_List.md)