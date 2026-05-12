import pytest
from CheckmarxPythonSDK.CxOne.apisecAPI import ApiSecAPI


class TestApiSecAPI:
    scan_id = "17f96629-159a-4d29-9cf3-873394372b2f"
    api_id = "787ce8d5-635f-4b82-af62-ca697979905b"
    group_column = "http_method"

    def setup_method(self):
        self.apisec_api = ApiSecAPI()

    @pytest.mark.xfail(reason="Server returns 500 for this scan_id / group_column combination")
    def test_get_grouped_risk_summary(self):
        grouped_summary = self.apisec_api.get_grouped_risk_summary(
            scan_id=self.scan_id, group_column=self.group_column
        )
        print(f"Total records: {grouped_summary.total_records}")
        print(f"Total pages: {grouped_summary.total_pages}")
        if grouped_summary.groups:
            for group in grouped_summary.groups:
                print(f"- {group.top_level_group_value}: {group.total_records}")
        assert grouped_summary is not None

    @pytest.mark.xfail(reason="Server returns 500 for this api_id")
    def test_get_api_parameters(self):
        api_parameters = self.apisec_api.get_api_parameters(api_id=self.api_id)
        if api_parameters.request_parameters:
            print(f"Request parameters: {len(api_parameters.request_parameters)}")
        if api_parameters.response_parameters:
            print(f"Response parameters: {len(api_parameters.response_parameters)}")
        if api_parameters.pii:
            print(f"PII: {len(api_parameters.pii)}")
        if api_parameters.api_origins:
            print(f"API origins: {len(api_parameters.api_origins)}")
        assert api_parameters is not None

    def test_get_risk_summary_by_origin(self):
        risk_summary = self.apisec_api.get_risk_summary_by_origin(scan_id=self.scan_id)
        if risk_summary.entries:
            for entry in risk_summary.entries:
                print(f"- {entry.name}: {entry.count}")
        assert risk_summary is not None

    def test_get_scan_apisec_risk_overview(self):
        risk_overview = self.apisec_api.get_scan_apisec_risk_overview(
            scan_id=self.scan_id
        )
        print(f"API count: {risk_overview.api_count}")
        print(f"Total risks count: {risk_overview.total_risks_count}")
        assert risk_overview is not None

    def test_get_all_risk_types(self):
        risk_types_response = self.apisec_api.get_all_risk_types(scan_id=self.scan_id)
        print(f"risk_types_response: {risk_types_response}")
        assert risk_types_response is not None

    def test_get_number_of_sensitive_data_apis(self):
        sensitive_data_count = self.apisec_api.get_number_of_sensitive_data_apis(
            scan_id=self.scan_id
        )
        print(f"Sensitive data count: {sensitive_data_count}")
        assert sensitive_data_count is not None

    def test_get_number_of_undocumented_apis(self):
        undocumented_count = self.apisec_api.get_number_of_undocumented_apis(
            scan_id=self.scan_id
        )
        print(f"Undocumented APIs count: {undocumented_count}")

    def test_get_all_api_scan_metadata(self):
        metadata = self.apisec_api.get_all_api_scan_metadata()
        print(f"Metadata entries: {len(metadata)}")
        for m in metadata:
            print(f"- column: {m.column}, options: {len(m.options)}")
        assert metadata is not None
