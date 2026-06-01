from dataclasses import dataclass


@dataclass
class DastScanAuthParameters:
    browser_id: str = None
    login_page_url: str = None
    login_page_wait: int = None
    min_wait_for: int = None
    script: str = None
    script_engine: str = None
    step_delay: int = None
    # Steps shape varies by Method and was empty in every observed env;
    # left as raw list until a populated example is available.
    steps: list = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanAuthParameters":
        return cls(
            browser_id=item.get("BrowserID"),
            login_page_url=item.get("LoginPageURL"),
            login_page_wait=item.get("LoginPageWait"),
            min_wait_for=item.get("MinWaitFor"),
            script=item.get("Script"),
            script_engine=item.get("ScriptEngine"),
            step_delay=item.get("StepDelay"),
            steps=item.get("Steps"),
        )
