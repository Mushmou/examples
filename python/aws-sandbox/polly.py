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
    Text=text,
    TextType='text',
    VoiceId='Joanna',
)
    # Save the audio to a file (optional)
    with open('output.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

    return response

text = "Hello, this is a sample text to be converted into speech."
response = text_to_speech(text)