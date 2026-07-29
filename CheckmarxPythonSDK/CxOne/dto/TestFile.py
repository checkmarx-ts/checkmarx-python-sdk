from dataclasses import dataclass


@dataclass
class TestFile:
    """A test file generated for the remediation."""

    file_path: str = None
    file_content: str = None
    test_type: str = None
    coverage_description: str = None
    framework_used: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "TestFile":
        return cls(
            file_path=item.get("file_path"),
            file_content=item.get("file_content"),
            test_type=item.get("test_type"),
            coverage_description=item.get("coverage_description"),
            framework_used=item.get("framework_used"),
        )
