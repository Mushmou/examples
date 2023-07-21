"""
export AWS_ACCESS_KEY_ID="AKIAXLJW4PA6GB5R7WM7",
export AWS_SECRET_ACCESS_KEY="Hx3lrTmg+hMuo1yr3rV2OZT1S6CC/0ictjLhXRQX"
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=your_default_region
"""
import boto3

# Specify the AWS region you want to use
region_name = 'us-west-2'  # Replace this with your desired AWS region

# Initialize the Polly client with the specified region
polly_client = boto3.client(
    'polly',
    region_name=region_name,
    )


def text_to_speech(text, output_format='mp3', voice_id='Joanna'):
    response = polly_client .synthesize_speech(
    OutputFormat='mp3',
    SampleRate='8000',
    Text='Hello, Noah',
    TextType='text',
    VoiceId='Joanna',
)
    # Save the audio to a file (optional)
    with open('output.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

    return response

text = "Hello, this is a sample text to be converted into speech."
response = text_to_speech(text)