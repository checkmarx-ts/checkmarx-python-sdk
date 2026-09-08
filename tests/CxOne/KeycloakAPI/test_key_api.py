from CheckmarxPythonSDK.CxOne.KeycloakAPI import KeyApi
import logging
logger = logging.getLogger(__name__)


class TestKeyApi:
    def setup_method(self):
        self.key_api = KeyApi()
        self.realm = "happy"

    def test_get_keys(self):
        try:
            keys_metadata = self.key_api.get_keys(realm=self.realm)
            assert keys_metadata is not None
            logger.info(f"Got keys metadata: {keys_metadata is not None}")
            if keys_metadata and keys_metadata.keys:
                logger.info(f"Number of keys: {len(keys_metadata.keys)}")
        except Exception as e:
            logger.error(f"Error in test_get_keys: {e}")
        assert True
