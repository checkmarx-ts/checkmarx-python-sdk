import pytest
from CheckmarxPythonSDK.CxOne.apisecAPI import ApiSecAPI
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
import logging
logger = logging.getLogger(__name__)


def _get_apisec_scan():
    """Return (scan_id, project_id) from a Completed scan that ran the
    apisec engine, or (None, None) if none is found."""
    result = _ScansAPI().get_a_list_of_scans(limit=30, statuses=["Completed"])
    for scan in result.scans:
        if "apisec" in (scan.engines or []):
            return scan.id, scan.project_id
    return None, None


class TestApiSecAPI:

    def setup_method(self):
        self.apisec_api = ApiSecAPI()
        self.scan_id, self.project_id = _get_apisec_scan()

    def test_get_risk_summary_by_origin(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risk_summary = self.apisec_api.get_risk_summary_by_origin(scan_id=self.scan_id)
        if risk_summary.entries:
            for entry in risk_summary.entries:
                logger.info(f"- {entry.name}: {entry.count}")
        assert risk_summary is not None

    def test_get_scan_apisec_risk_overview(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risk_overview = self.apisec_api.get_scan_apisec_risk_overview(
            scan_id=self.scan_id
        )
        logger.info(f"API count: {risk_overview.api_count}")
        logger.info(f"Total risks count: {risk_overview.total_risks_count}")
        assert risk_overview is not None

    def test_get_all_risk_types(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risk_types_response = self.apisec_api.get_all_risk_types(scan_id=self.scan_id)
        logger.info(f"risk_types_response: {risk_types_response}")
        assert risk_types_response is not None

    def test_get_number_of_sensitive_data_apis(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        sensitive_data_count = self.apisec_api.get_number_of_sensitive_data_apis(
            scan_id=self.scan_id
        )
        logger.info(f"Sensitive data count: {sensitive_data_count}")
        assert sensitive_data_count is not None

    def test_get_number_of_undocumented_apis(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        undocumented_count = self.apisec_api.get_number_of_undocumented_apis(
            scan_id=self.scan_id
        )
        logger.info(f"Undocumented APIs count: {undocumented_count}")

    def test_get_all_api_scan_metadata(self):
        metadata = self.apisec_api.get_all_api_scan_metadata()
        logger.info(f"Metadata entries: {len(metadata)}")
        for m in metadata:
            logger.info(f"- column: {m.column}, options: {len(m.options)}")
        assert metadata is not None

    def test_get_api_security_risks_by_scan_id(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risks = self.apisec_api.get_api_security_risks_by_scan_id(
            scan_id=self.scan_id, per_page=5
        )
        assert risks is not None
        logger.info(f"Total records: {risks.total_records}")

    def test_get_risk_detail_by_risk_id(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risks = self.apisec_api.get_api_security_risks_by_scan_id(
            scan_id=self.scan_id, per_page=1
        )
        if not risks.entries:
            pytest.skip("Scan has no API Security risks")
        detail = self.apisec_api.get_risk_detail_by_risk_id(
            risk_id=risks.entries[0].risk_id
        )
        assert detail is not None

    def test_get_risk_complete(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risks = self.apisec_api.get_api_security_risks_by_scan_id(
            scan_id=self.scan_id, per_page=1
        )
        if not risks.entries:
            pytest.skip("Scan has no API Security risks")
        complete = self.apisec_api.get_risk_complete(
            scan_id=self.scan_id, risk_id=risks.entries[0].risk_id
        )
        assert complete is not None
        assert complete.risk_id == risks.entries[0].risk_id

    def test_get_grouped_risk_summary(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        grouped_summary = self.apisec_api.get_grouped_risk_summary(
            scan_id=self.scan_id, group_column="severity"
        )
        logger.info(f"Total records: {grouped_summary.total_records}")
        logger.info(f"Total pages: {grouped_summary.total_pages}")
        if grouped_summary.groups:
            for group in grouped_summary.groups:
                logger.info(f"- {group.top_level_group_value}: {group.total_records}")
        assert grouped_summary is not None

    def test_get_grouped_risk_summary_sorting_order(self):
        """sorting_order is the correct param name for this endpoint
        (unlike the sibling get_api_security_risks_by_scan_id, which
        uses `sorting`) -- the server 500s if the wrong name is sent.
        """
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        asc = self.apisec_api.get_grouped_risk_summary(
            scan_id=self.scan_id, group_column="severity", sorting_order="asc"
        )
        desc = self.apisec_api.get_grouped_risk_summary(
            scan_id=self.scan_id, group_column="severity", sorting_order="desc"
        )
        asc_values = [g.top_level_group_value for g in (asc.groups or [])]
        desc_values = [g.top_level_group_value for g in (desc.groups or [])]
        if len(asc_values) > 1:
            assert asc_values == list(reversed(desc_values))

    def test_get_api_parameters(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risks = self.apisec_api.get_api_security_risks_by_scan_id(
            scan_id=self.scan_id, per_page=1
        )
        if not risks.entries:
            pytest.skip("Scan has no API Security risks")
        api_parameters = self.apisec_api.get_api_parameters(
            api_id=risks.entries[0].api_id
        )
        if api_parameters.request_parameters:
            logger.info(f"Request parameters: {len(api_parameters.request_parameters)}")
        if api_parameters.response_parameters:
            logger.info(f"Response parameters: {len(api_parameters.response_parameters)}")
        if api_parameters.pii:
            logger.info(f"PII: {len(api_parameters.pii)}")
        if api_parameters.api_origins:
            logger.info(f"API origins: {len(api_parameters.api_origins)}")
        assert api_parameters is not None

    def test_get_parameters(self):
        if not self.scan_id:
            pytest.skip("No completed API Security scan found")
        risks = self.apisec_api.get_api_security_risks_by_scan_id(
            scan_id=self.scan_id, per_page=1
        )
        if not risks.entries:
            pytest.skip("Scan has no API Security risks")
        params = self.apisec_api.get_parameters(api_id=risks.entries[0].api_id)
        assert params is not None
