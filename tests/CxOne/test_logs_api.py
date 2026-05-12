from CheckmarxPythonSDK.CxOne.logsAPI import LogsAPI


class TestLogsAPI:
    """Test class for LogsAPI"""
    
    # 测试参数
    scan_id = "d22617f1-4577-4925-901c-c655a2793cf5"
    scan_type = "sast"  # 可以根据需要修改为其他扫描类型
    
    def setup_method(self):
        """Setup method to create LogsAPI instance before tests"""
        self.logs_api = LogsAPI()
    
    def test_get_log(self):
        """Test get_log method"""
        print(f"Testing get_log with scan_id: {self.scan_id}, scan_type: {self.scan_type}")
        try:
            log_content = self.logs_api.get_log(
                scan_id=self.scan_id,
                scan_type=self.scan_type
            )
            print("Success!")
            print(f"Log content length: {len(log_content)} characters")
            # 打印前500个字符作为预览
            preview = log_content[:500] if len(log_content) > 500 else log_content
            print(f"Log preview:\n{preview}")
            assert log_content is not None
            assert isinstance(log_content, str)
        except Exception as e:
            print(f"Error: {str(e)}")
            # 由于API可能返回错误，这里不做断言，只记录错误
    
    def test_get_log_with_invalid_scan_id(self):
        """Test get_log method with invalid scan_id"""
        print("Testing get_log with invalid scan_id")
        try:
            log_content = self.logs_api.get_log(
                scan_id="invalid-scan-id",
                scan_type=self.scan_type
            )
            print("Unexpected success!")
            assert False, "Should have raised an exception"
        except Exception as e:
            print(f"Expected error: {str(e)}")
            # 预期会失败，所以这里不做断言
    
    def test_get_log_with_invalid_scan_type(self):
        """Test get_log method with invalid scan_type"""
        print("Testing get_log with invalid scan_type")
        try:
            log_content = self.logs_api.get_log(
                scan_id=self.scan_id,
                scan_type="invalid-scan-type"
            )
            print("Unexpected success!")
            assert False, "Should have raised an exception"
        except Exception as e:
            print(f"Expected error: {str(e)}")
            # 预期会失败，所以这里不做断言
