import abc
import requests
import base64


class TextToSpeech():

    def __init__(self, req: requests) -> None:
        """Initialize Class"""
        self.validate_request(req)

    @abc.abstractmethod
    def validate_request(self, req: requests):
        """Validate Request"""

    @abc.abstractmethod
    def speech(self, text: str, language: str) -> bytes:
        """Speech """


class Google(TextToSpeech):
    """Google API"""

    def validate_request(self, req):
        pass

    def speech(self, text, language) -> bytes:
        print("hi ngoc")
        audio_stream = None
        return audio_stream


class Azure(TextToSpeech):
    """Azure API"""

    def validate_request(self, req):
        pass

    def speech(self, text, language) -> bytes:
        audio_stream = None
        return audio_stream


class AWS(TextToSpeech):
    """AWS API"""

    def validate_request(self, req):
        """
        validate request to
        Input: e
        """
        # if not req.payload.get("api_key"):
        #     raise ValueError("Missing API_KEY"]
        # self.key = req.payload.get("api_key")
        pass

    def speech(self, text, language) -> bytes:

        audio_stream = None
        return audio_stream


def validate_common(req):
    """Validate stuff that has nothing to do with the providers."""
    if not req.payload.get("text"):
        raise ValueError("Missing Text")
    if not req.payload.get("lang"):
        raise ValueError("Missing Language")
    return (req.payload.get("text"), req.payload.get("lang"))


IMPLEMENTATIONS = {
    "google": Google,
    "azure": Azure,
    "aws": AWS,
}


def main(req, res):
    try:
        text, language = validate_common(req)
    except (ValueError) as value_error:
        return res.json({
            "success": False,
            "error": f"{value_error}",
        })
    res = IMPLEMENTATIONS[req.payload.get("provider")](req)
    print(res)
    print(res.speech(text, language))

    # try:
        # res = IMPLEMENTATIONS[req.payload.get("provider")](req)
    # except Exception as error:
    #     return res.json({
    #         "success": False,
    #         "error": f"{type(error).__name__}: {error}",
    #     })

    # return res.json({
    #     "success": True,
    #     "image": base64.b64encode(res.audio_stream).decode(),
    # })


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


# Google Request
req = MyRequest({
    "payload": {
        "provider": "google",
        "text": "hi",
        "lang": "English",
    },
    "variables": {
        "API_KEY": "1234"
    }
})

main(req, None)