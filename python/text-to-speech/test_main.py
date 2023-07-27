# Standard library
import base64
import unittest
import pathlib
from unittest.mock import patch

# Third party
import requests
from parameterized import parameterized
from google.cloud import texttospeech


# Local imports
import main
import secret

RESULT_GOOGLE = (
    pathlib.Path("python/text-to-speech/results/google.txt").
    read_text(encoding="utf-8"))

# Path to krakenio encoded result (str).
RESULT_AZURE = (
    pathlib.Path("python/text-to-speech/results/azure.txt").
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


class GoogleTest(unittest.TestCase):
    """Google API Test Cases"""
    def test_validate_request(self, mock_client):
        pass

    def test_validate_request_missing_project_id(self, req):
        """Test validate_request method when 'PROJECT_ID' is missing."""
        pass

    def test_validate_request_missing_api_key(self, req):
        """Test validate_request method when 'API_KEY' is missing."""
        pass

    def test_speech_happy(self):
        """Test speech method for successful text-to-speech synthesis."""
        req = MyRequest({
            "payload": {
                "provider": "google",
                "text": "hi",
                "language": "en-US",
            },
            "variables": {
                "API_KEY": "123",
                "PROJECT_ID": "123",
            }
        })
        # Create an instance of Google Class
        google_instance = main.Google(req)
        # Variables
        text = "Hi"
        language = "en-US"
        # Set up mock
        with patch.object(texttospeech, "TextToSpeechClient") as mock_client:
            mock_response = mock_client.return_value
            mock_response.synthesize_speech.return_value.audio_content = base64.b64decode(RESULT_GOOGLE)

            # Call the speech method
            audio_stream = google_instance.speech(text, language)

            # Assert that the mock client was called with the correct arguments
            mock_client.assert_called_once_with(client_options={"api_key": "123", "quota_project_id": "123"})

            # Assert that the synthesize_speech method was called with the correct arguments
            mock_response.synthesize_speech.assert_called_once_with(input=texttospeech.SynthesisInput(text=text),
                                                                voice=texttospeech.VoiceSelectionParams(language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL),
                                                                audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))

            # Assert the result
            self.assertEqual(audio_stream, mock_response.synthesize_speech.return_value.audio_content)

    def test_speech_error(self, text, language):
        """Test speech method for handling errors during text-to-speech synthesis."""
        pass


class AzureTest(unittest.TestCase):
    """Azure API Test Cases"""
    def test_validate_request(self, req):
        """Test validate_request method when all required fields are present."""
        pass

    def test_validate_request_missing_speech_key(self, req):
        """Test validate_request method when 'API_KEY' is missing."""
        pass

    def test_validate_request_missing_region_key(self, req):
        """Test validate_request method when 'REGION_KEY' is missing."""
        pass

    def test_speech_happy(self, text, language):
        """Test speech method for successful text-to-speech synthesis."""
        pass

    def test_speech_error(self, text, language):
        """Test speech method for handling errors during text-to-speech synthesis."""
        pass


class AWSTest(unittest.TestCase):
    """AWS API Test Cases"""
    def test_validate_request(self, req):
        """Test validate_request method when all required fields are present."""
        pass

    def test_validate_request_missing_aws_access_key_id(self, req):
        """Test validate_request method when 'AWS_ACCESS_KEY_ID' is missing."""
        pass

    def test_validate_request_missing_aws_secret_access_key(self, req):
        """Test validate_request method when 'AWS_SECRET_ACCESS_KEY' is missing."""
        pass

    def test_speech(self, text, language):
        """Test speech method for text-to-speech synthesis."""
        pass

    def test_speech_key_exception(self, text, language):
        """Test speech method for handling exceptions during text-to-speech synthesis."""
        pass


class ValidateCommonTest(unittest.TestCase):
    """Test Cases for validate_common function"""
    def test_validate_common(self, req):
        """Test validate_common function with valid input."""
        pass

    def test_missing_text(self, req):
        """Test validate_common function when 'text' is missing."""
        pass

    def test_missing_language(self, req):
        """Test validate_common function when 'language' is missing."""
        pass


class MainTest(unittest.TestCase):
    """Test Cases for main function."""
    @unittest.skipUnless(secret.GOOGLE_API_KEY, "No Google API Key set.")
    def test_main(self):
        """Unittest for main function success json response."""
        want = {
            "success": True,
            "audio_stream": RESULT_GOOGLE,
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
        res = MyResponse()
        main.main(req, res)

        # Check the response
        got = res.json()
        self.assertFalse(got["success"])
        self.assertIn("AccountError", got["error"])

if __name__ == "__main__":
    unittest.main()
