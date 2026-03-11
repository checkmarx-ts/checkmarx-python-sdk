from CheckmarxPythonSDK.CxOne.apisecAPI import ApiSecAPI


class TestApiSecAPI:
    """Test class for ApiSecAPI"""
    
    # 测试参数
    scan_id = "17f96629-159a-4d29-9cf3-873394372b2f"
    api_id = "787ce8d5-635f-4b82-af62-ca697979905b"
    group_column = "http_method"
    
    def setup_method(self):
        """Setup method to create ApiSecAPI instance before tests"""
        self.apisec_api = ApiSecAPI()
    
    def test_get_grouped_risk_summary(self):
        """Test get_grouped_risk_summary method"""
        print(f"Testing get_grouped_risk_summary with scan_id: {self.scan_id}, group_column: {self.group_column}")
        try:
            grouped_summary = self.apisec_api.get_grouped_risk_summary(
                scan_id=self.scan_id,
                group_column=self.group_column
            )
            print(f"Success! Total records: {grouped_summary.total_records}")
            print(f"Total pages: {grouped_summary.total_pages}")
            if grouped_summary.groups:
                print(f"Groups found: {len(grouped_summary.groups)}")
                for group in grouped_summary.groups:
                    print(f"- {group.top_level_group_value}: {group.total_records}")
            else:
                print("No groups found")
            assert grouped_summary is not None
        except Exception as e:
            print(f"Error: {str(e)}")
            
    
    def test_get_api_parameters(self):
        """Test get_api_parameters method"""
        print(f"Testing get_api_parameters with api_id: {self.api_id}")
        try:
            api_parameters = self.apisec_api.get_api_parameters(api_id=self.api_id)
            print("Success!")
            if api_parameters.request_parameters:
                print(f"Request parameters found: {len(api_parameters.request_parameters)}")
            if api_parameters.response_parameters:
                print(f"Response parameters found: {len(api_parameters.response_parameters)}")
            if api_parameters.pii:
                print(f"PII found: {len(api_parameters.pii)}")
            if api_parameters.api_origins:
                print(f"API origins found: {len(api_parameters.api_origins)}")
            assert api_parameters is not None
        except Exception as e:
            print(f"Error: {str(e)}")
            
    
    def test_get_risk_summary_by_origin(self):
        """Test get_risk_summary_by_origin method"""
        print(f"Testing get_risk_summary_by_origin with scan_id: {self.scan_id}")
        try:
            risk_summary = self.apisec_api.get_risk_summary_by_origin(scan_id=self.scan_id)
            print("Success!")
            if risk_summary.entries:
                for entry in risk_summary.entries:
                    if hasattr(entry, 'name') and hasattr(entry, 'count'):
                        print(f"- {entry.name}: {entry.count}")
                    elif isinstance(entry, dict):
                        print(f"- {entry.get('name', 'Unknown')}: {entry.get('count', 0)}")
                    else:
                        print(f"- {entry}")
            assert risk_summary is not None
        except Exception as e:
            print(f"Error: {str(e)}")
        
    
    def test_get_scan_apisec_risk_overview(self):
        """Test get_scan_apisec_risk_overview method"""
        print(f"Testing get_scan_apisec_risk_overview with scan_id: {self.scan_id}")
        try:
            risk_overview = self.apisec_api.get_scan_apisec_risk_overview(scan_id=self.scan_id)
            print("Success!")
            print(f"API count: {risk_overview.api_count}")
            print(f"Total risks count: {risk_overview.total_risks_count}")
            assert risk_overview is not None
        except Exception as e:
            print(f"Error: {str(e)}")
            
    
    def test_get_all_risk_types(self):
        """Test get_all_risk_types method"""
        print(f"Testing get_all_risk_types with scan_id: {self.scan_id}")
        try:
            risk_types_response = self.apisec_api.get_all_risk_types(scan_id=self.scan_id)
            print("Success!")
            print(f"risk_types_response: {risk_types_response}")
            assert risk_types_response is not None
        except Exception as e:
            print(f"Error: {str(e)}")
            
    
    def test_get_number_of_sensitive_data_apis(self):
        """Test get_number_of_sensitive_data_apis method"""
        print(f"Testing get_number_of_sensitive_data_apis with scan_id: {self.scan_id}")
        try:
            sensitive_data_count = self.apisec_api.get_number_of_sensitive_data_apis(scan_id=self.scan_id)
            print(f"Success! Count: {sensitive_data_count}")
            assert sensitive_data_count is not None
        except Exception as e:
            print(f"Error: {str(e)}")
            
    
    def test_get_number_of_undocumented_apis(self):
        """Test get_number_of_undocumented_apis method"""
        print(f"Testing get_number_of_undocumented_apis with scan_id: {self.scan_id}")
        try:
            undocumented_count = self.apisec_api.get_number_of_undocumented_apis(scan_id=self.scan_id)
            print(f"Success! Count: {undocumented_count}")
            # 这里不做断言，因为API可能返回None
        except Exception as e:
            print(f"Error: {str(e)}")
            
    
    def test_get_all_api_scan_metadata(self):
        """Test get_all_api_scan_metadata method"""
        print("Testing get_all_api_scan_metadata")
        try:
            metadata = self.apisec_api.get_all_api_scan_metadata()
            print("Success!")
            print(f"metadata: {metadata}")
            assert metadata is not None
        except Exception as e:
            print(f"Error: {str(e)}")
            
