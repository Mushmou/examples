# Standard Library
import base64

# Third Party
from google.cloud import texttospeech
import azure.cognitiveservices.speech as speechsdk
import boto3

# Local Imports
import secret.py

"""
Aws -> AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

"""

class text_to_speech:
    def __init__(self, req) -> None:
        pass
    def aws(self, variables) -> bytes:
        pass
    def google(self, variables) -> bytes:
        pass
    def azure(self, variables) -> bytes:
        pass
    def validate_request(self, req) -> dict:
        """
        
        """
        pass


def main(req, res) -> any:
    """
    The main function that runs the text to speech function.

    Input:
        req (json): contains payload and variables
            payload includes: provider, language, text
        res (json): contains the response object.
    """
    pass