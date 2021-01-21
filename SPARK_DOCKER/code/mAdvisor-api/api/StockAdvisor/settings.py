

# natural_language_understanding_settings = {
#           "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
#           "username": "edf8e7fc-7fe9-4f8e-93a2-d68497fa15a2",
#           "password": "BBeXnQU70YFf"
#         }

# natural_language_understanding_settings = {
#           "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
#           "username": "ec09107d-e627-4c78-ad3b-38c1b3ffca45",
#           "password": "7s6GbZjamUO8"
#         }
import environ
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env('config/settings/.env')

natural_language_understanding_settings = {
  "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
  "username": env('NLU_USERNAME'),
  "password": env('NLU_PASSWORD')
}


voice_to_text_settings = {
        "url": "https://stream.watsonplatform.net/speech-to-text/api",
        "username": env('VOICE_TO_TEXT_USERNAME'),
        "password": env('VOICE_TO_TEXT_PASSWORD')
        }

NUMBEROFTRIES = 10

CACHESALT = "vivek"

TEMPDIR = "temp/"
