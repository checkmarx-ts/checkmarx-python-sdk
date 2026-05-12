import asyncio
import aiohttp
import requests
from CheckmarxPythonSDK.async_api_client import AsyncApiClient
from CheckmarxPythonSDK.CxOne.projectsAPI import ProjectsAPI
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class RequestData:
    def __init__(
        self,
        method: str,
        url: str,
        param: dict,
        json: str = None,
        description: str = None,
    ):
        self.method = method
        self.url = url
        self.param = param
        self.json = json
        self.description = description


class ApiData:
    def __init__(
        self, request_data: RequestData, response_handler: Callable[[dict], dict] = None
    ):
        self.request_data = request_data
        self.response_handler = response_handler


api_data = ApiData(
    request_data=RequestData(
        method="GET", url="/projects", param={}, json={}, description="Get all projects"
    ),
    response_handler=None,
)

response = requests.session().request(
    method=api_data.request_data.method,
    url=api_data.request_data.url,
    params=api_data.request_data.param,
    json=api_data.request_data.json,
)
print(response.json())
# response to ProjectsCollection


async def main():
    # A ClientSession is used for making multiple requests within a single session
    async with aiohttp.ClientSession() as session:
        # Use 'async with' to ensure the response is properly closed
        async with session.request(
            method=api_data.request_data.method,
            url=api_data.request_data.url,
            params=api_data.request_data.param,
            json=api_data.request_data.json,
        ) as response:
            print(f"Status: {response.status}")
            print(f"Content type: {response.headers['content-type']}")

            # Use await to get the JSON data asynchronously
            data = await response.json()
            print(
                f"Location: {data['iss_position']['latitude']}, {data['iss_position']['longitude']}"
            )
            # response to ProjectsCollection


# Run the main coroutine using the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
