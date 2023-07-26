# Standard library
import base64
import unittest
from unittest.mock import patch

# Third party
import requests
from parameterized import parameterized

# Local imports
import main

RESULT_GOOGLE = (
    pathlib.Path("result/google.txt").
    read_text(encoding="utf-8"))

# Path to krakenio encoded result (str)
RESULT_GOOGLE = (
    pathlib.Path("result/azure.txt").
    read_text(encoding="utf-8"))

class MyRequest:
	"""Class for defining My Request structure."""

	def __init__(self, data):
		self.payload = data.get("payload", {})
		self.variables = data.get("variables", {})


class MyResponse:
	"""Class for defining My Response structure."""

	def __init__(self):
		self._json = None

	def json(self, data=None):
		"""Create a response for json."""
		if data is not None:
			self._json = data
		return self._json

class GoogleTest(TextToSpeech):
  """Google API"""
  	def test_validate_request(self, req):
      	pass
	def test_validate_request_missing_project_id(self, req):
		pass
	def test_validate_request_missing_api_key(self, req):
		pass
  	def test_speech_happy(self, text, language):
		pass
	def test_speech_error(self, text, language):
		pass

class AzureTest(TextToSpeech):
    """Azure API"""
    def test_validate_request(self, req):
        pass
	def test_validate_request_missing_speech_key(self, req):
		pass
	def test_validate_request_missing_region_key(self, req):
		pass
    def test_speech_happy(self, text, language):
		pass
	def test_speech_error(self, text, language):
		pass


class AWSTest(TextToSpeech):
    """AWS API"""
    def test_validate_request(self, req):
        pass
	def test_validate_request_missing_aws_access_key_id(self, req):
		pass
	def test_validate_request_missing_aws_secret_access_key(self, req):
		pass
    def test_speech(self, text, language):
		pass
	def test_speech_key_exception(self, text, language):
		pass


class ValidateCommonTest(req):
	def test_validate_common(self, req):
		pass
	def test_missing_text(self, req):
		pass
	def test_missing_language(self, req):
		pass

class MainTest(req, res):
    """Class test for main function."""
    @unittest.skipUnless(secret.GOOGLE_API_KEY, "No Google API Key set.")
    def test_main(self):
        """Unittest for main function success json response."""
        want = {
            "success": True,
            "audio_stream": GOOGLE_RESULT,
        }
        # Create a request
        req = MyRequest({
            "payload": {
                "provider": "google",
                "text": "hi",
				"language": "en-US",
            },
            "variables": {
                "API_KEY": secret.API_KEY_TINYPNG,
				"PROJECT_ID": secret.GOOGLE_API_KEY,
            }
        })
        # Create a response object
        res = MyResponse()
        main.main(req, res)
        # Check the response
        got = res.json()
        self.assertEqual(got, want)

    def test_main_value_error(self):
        """Unittest for main function when a value error is raised."""
        want = {"success": False, "error": "Missing payload"}
        # Create a request
        req = MyRequest({"payload": {}, "variables": {}})
        # Create a response object
        res = MyResponse()
        main.main(req, res)

        # Check the response
        got = res.json()
        self.assertEqual(got, want)

    def test_main_exception(self):
        """Unittest case for main function when exception is raised."""
        # Create a request
        req = MyRequest({
            "payload": {
                "provider": "tinypng",
                "image": base64.b64encode(IMAGE).decode()
            },
            "variables": {
                "API_KEY": "wrong_api_key"
            }
        })
        # Create a response object
        res = MyResponse()  # Create a response object
        main.main(req, res)

        # Check the response
        got = res.json()
        self.assertFalse(got["success"])
        self.assertIn("AccountError", got["error"])
if __name__ == "__main__":
    unittest.main()
