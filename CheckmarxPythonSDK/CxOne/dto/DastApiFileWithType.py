from dataclasses import dataclass
from typing import Dict, Optional

from .DastFileInfo import DastFileInfo


@dataclass
class DastApiFileWithType:
    """An entry in `apiFiles[]` on GET /authSession/{envId} and the
    response of GET /authSession/{envId}/apiFilesData.

    Attributes:
        file (Optional[DastFileInfo]): The file itself.
        api_type (Optional[str]): OPENAPI, POSTMAN, HAR, SOAP, or GRAPHQL.
        api_url (Optional[str]): The API's base URL, if applicable.
        api_variables (Dict[str, str]): Variable substitutions for the file.
    """
    file: Optional[DastFileInfo] = None
    api_type: Optional[str] = None
    api_url: Optional[str] = None
    api_variables: Dict[str, str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastApiFileWithType":
        return cls(
            file=DastFileInfo.from_dict(item["file"]) if item.get("file") else None,
            api_type=item.get("apiType"),
            api_url=item.get("apiURL"),
            api_variables=item.get("apiVariables"),
        )
