before testing, we should set some pre-requisites for test.
    1. create custom field "ProjectManager" from WebPortal
    2. prepare a shared folder ( another windows system in the same domain)
            \\WIN-4MUJCQQ4KNT\Users\Administrator\Downloads\CxShare
    3. prepare the source control repositories, with username and password.
    4. prepare the git pull batch script, and a Pre scan action, for the source pulling
        pre-scan action name:   git
        the batch script in Checkmarx/Executables folder: gitPull.bat
    5. Install another engine, get the engine url,
        http://192.168.43.113/CxSourceAnalyzerEngineWCF/CxEngineWebServices.svc

    source code sources:
        I. local:   the zip file, JavaVulnerableLab-master.zip
        II. shared:  \\WIN-4MUJCQQ4KNT\Users\Administrator\Downloads\CxShare
        III. source control:
            1. git   https://github.com/CSPF-Founder/JavaVulnerableLab.git
            2. svn
            3. tfs
            4. perforce
        IV. source pulling:

    JIRA:
        name: REST_API_SDK_TEST
        key: CX
