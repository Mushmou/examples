"""Synthesize text to speech using Google, Azure and AWS API."""
# Standard library
import base64
import abc
import json

# Third party
import requests
from google.cloud import texttospeech
import boto3


class TextToSpeech():
    """Base class for Text to Speech."""
    def __init__(self, req: requests) -> None:
        """Initialize class method."""
        self.validate_request(req)

    @abc.abstractmethod
    def validate_request(self, req: requests) -> None:
        """Abstract validate request method for providers."""

    @abc.abstractmethod
    def speech(self, text: str, language: str) -> bytes:
        """Abstract speech method for providers."""


class Google(TextToSpeech):
    """This class represents the implementation of Google text to speech."""
    def validate_request(self, req: requests) -> None:
        """
        This method validates the request data for Google text to speech.

        Input:
            req (request): The request provided by the user.

        Raises:
            ValueError: If any required value is missing or invalid.
        """
        if not req.variables.get("API_KEY"):
            raise ValueError("Missing API_KEY.")
        if not req.variables.get("PROJECT_ID"):
            raise ValueError("Missing PROJECT_ID.")
        self.api_key = req.variables.get("API_KEY")
        self.project_id = req.variables.get("PROJECT_ID")

    def speech(self, text: str, language: str) -> bytes:
        """
        Converts the given text into speech with the Google text to speech API.

        Input:
            text: The text to be converted into speech.
            language: The language code (BCP-47 format).

        Returns:
            bytes: The synthezied speech in bytes.
        """
        # Instantiate a client.
        client = texttospeech.TextToSpeechClient(client_options={
            "api_key": self.api_key,
            "quota_project_id": self.project_id,
        })
        # Set the text input to be synthesized.
        synthesis_input = texttospeech.SynthesisInput(text=text)
        # Build the voice request, select the language code ("en-US")
        # and the ssml voice gender is neutral.
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        # Select the type of audio file you want returned.
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)
        # Perform the text-to-speech request on the text input
        # with the selected voice parameters and audio file type.
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        return response.audio_content


class Azure(TextToSpeech):
    """This class represents the implementation of Azure text to speech."""
    def validate_request(self, req: requests) -> None:
        """
        This method validates the request data for Azure text to speech.

        Input:
            req (request): The request provided by the user.
        Raises:
            ValueError: If any required value is missing or invalid.
        """
        if not req.variables.get("API_KEY"):
            raise ValueError("Missing API_KEY.")
        if not req.variables.get("REGION_KEY"):
            raise ValueError("Missing REGION_KEY.")
        self.api_key = req.variables.get("API_KEY")
        self.region_key = req.variables.get("REGION_KEY")

    def get_token(self, subscription_key):
        fetch_token_url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        access_token = str(response.text)
        return access_token

    def speech(self, text: str, language: str) -> bytes:
        """
        Converts the given text into speech with the Google text to speech API.

        Input:
            text: The text to be converted into speech.
            language: The language code (BCP-47 format).

        Returns:
            bytes: The synthezied speech in bytes.
        """
        url = f"https://{self.region_key}.tts.speech.microsoft.com/cognitiveservices/v1"

        headers_azure = {
            'Content-type': 'application/ssml+xml',
            # 'Ocp-Apim-Subscription-Key': self.api_key,
            'Authorization': 'Bearer ' + self.get_token(self.api_key),
            'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3',
        }
        data_azure = f"<speak version='1.0' xml:lang='{language}'><voice xml:lang='{language}' xml:gender='Male' name='en-US-ChristopherNeural'>{text}</voice></speak>"
        response = requests.request("POST", url, headers=headers_azure, data=data_azure)
        return response.content


class AWS(TextToSpeech):
    """This class represents the implementation of AWS text to speech. """
    voice_id = "Joanna"

    def validate_request(self, req: requests) -> None:
        """
        This method validates the request data for AWS text to speech.

        Input:
            req (request): The request provided by the user.
        Raises:
            ValueError: If any required value is missing or invalid.
        """
        if not req.variables.get("API_KEY"):
            raise ValueError("Missing API_KEY.")
        if not req.variables.get("SECRET_API_KEY"):
            raise ValueError("Missing SECRET_API_KEY.")
        self.api_key = req.variables.get("API_KEY")
        self.secret_api_key = req.variables.get("SECRET_API_KEY")

    def speech(self, text: str, language: str) -> bytes:
        """
        Converts the given text into speech with the AWS text to speech API.

        Input:
            text: The text to be converted into speech.
            language: The language code (BCP-47 format).

        Returns:
            bytes: The synthezied speech in bytes.
        """
        # Call polly client using boto3.session
        polly_client = boto3.Session(
            aws_access_key_id=self.api_key,
            aws_secret_access_key=self.secret_api_key,
            region_name="us-west-2").client("polly")

        # Get response from polly client
        response = polly_client.synthesize_speech(
            VoiceId=AWS.voice_id,
            OutputFormat="mp3",
            Text=text,
            LanguageCode=language
        )
        return response["Audiostream"]


list_of_providers = ["google", "azure", "aws"]


def validate_common(req: requests) -> tuple:
    """
    This function validates the common fields in the request data
        that are independent of the text-to-speech provider.

    Input:
        req (request): The request provided by the user.

    Returns:
        (tuple): A tuple containing the text and language from the request.

    Raises:
        ValueError: If any of the common fields (provider, text, language)
        are missing in the request payload.
    """
    # Check if the payload is empty.
    if not req.payload:
        raise ValueError("Missing Payload.")

    # Check if variables is empty.
    if not req.variables:
        raise ValueError("Missing Variables.")

    # Check if provider is empty.
    if not req.payload.get("provider"):
        raise ValueError("Missing Provider.")

    # Check if provider is in the list
    if (req.payload.get("provider").lower() not in list_of_providers):
        raise ValueError("Invalid Provider.")

    # Check if text is empty.
    if not req.payload.get("text"):
        raise ValueError("Missing Text.")

    # Check if language is empty.
    if not req.payload.get("language"):
        raise ValueError("Missing Language.")

    # Return the text and langage.
    return (req.payload.get("provider").lower(),
            req.payload.get("text"), req.payload.get("language"))


def main(req: requests, res: json) -> json:

    """
    Main Function for Text to Speech.

    Input:
        req(request): The request from the user.
        res(json): The response for the user.

    Returns:
        (json): JSON representing the success value of the text to speech api
        containing the synthesized audio in base64 encoded format.
    """
    try:
        provider, text, language = validate_common(req)
        if provider == "google":
            provider_class = Google(req)
        elif provider == "azure":
            provider_class = Azure(req)
        else:
            provider_class = AWS(req)

    except (ValueError) as value_error:
        return res.json({
            "success": False,
            "error": str(value_error),
        })
    try:
        audio_bytes = provider_class.speech(text, language)
    except Exception as error:
        return res.json({
            "success": False,
            "error": f"{type(error).__name__}: {error}",
        })

    return res.json({
        "success": True,
        "audio_bytes": base64.b64encode(audio_bytes).decode(),
    })
