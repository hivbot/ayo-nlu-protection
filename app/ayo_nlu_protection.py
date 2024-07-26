import spacy
import os
import requests
import json
import logging
from spacy.lang.en.examples import sentences
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig



from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

AYO_WHATSAPP_API = os.environ.get('AYO_WHATSAPP_API')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID')
VF_DM_URL = os.environ.get('VF_DM_URL')
VF_API_KEY = os.environ.get('VF_API_KEY')
VF_VERSION_ID = os.environ.get('VF_VERSION_ID')

ENTITIES = ["CREDIT_CARD", "CRYPTO",
            "EMAIL_ADDRESS", "IBAN_CODE",
            "IP_ADDRESS",
            "NRP", "LOCATION",
            "PERSON", "PHONE_NUMBER",
            "MEDICAL_LICENSE", "URL"]

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def analyze_text(text):
    analyze_result = analyzer.analyze(text=text,
                               entities=ENTITIES,
                               language='en',
                               score_threshold=0.5
                               )
    return analyze_result

def anonymize_text(text, results):
    anonymize_result = anonymizer.anonymize(text=text, analyzer_results=results,
                                           operators={"DEFAULT": OperatorConfig("replace")})
    return anonymize_result.text


def patch_user_variables(user_id, user_name):
    url = f"{VF_DM_URL}/state/user/{requests.utils.quote(user_id)}/variables"
    headers = {
        "Authorization": VF_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "user_id": user_id,
        "user_name": user_name
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response


def post_user_enquiry(DMconfig, session, user_id, user_enquiry):
    url = f"{VF_DM_URL}/state/user/{requests.utils.quote(user_id)}/interact",
    headers = {
        "Authorization": VF_API_KEY,
        "Content-Type": "application/json",
        "versionID": VF_VERSION_ID,
        "sessionID": session,
    },
    user_enquiry = str(user_enquiry['payload'])
    analyzed_text = analyze_text(user_enquiry)
    anonymized_text = anonymize_text(user_enquiry, analyzed_text)
    logger.info("anonymized_text: %s", anonymized_text)

    data = {
        "action": anonymized_text,
        "config": DMconfig,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


if __name__ == "__main__":
    user_input = ('Hello, my name is David Johnson and I live in Maine.',
               'My credit card number is 4095-2609-9393-4932 and my crypto wallet id is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ',
               'On September 18 I visited microsoft.com and sent an email to test@presidio.site,  from the IP 192.168.0.1.',
               'My passport: 191280342 and my phone number: (212) 555-1234.',
               'This is a valid International Bank Account Number: IL150120690000003111111 .',
               'Can you please check the status on bank account 954567876544?',
               "Kate's social security number is 078-05-1126.  Her driver license? it is 1234567A.")
    user_input = str(user_input)
    print("analyzer Result: ")
    text_analyzed = analyze_text(user_input)
    print(text_analyzed)
    print("anonymizer Result: ")
    text_anonymized = anonymize_text(user_input, text_analyzed)
    print(text_anonymized)

### Specified example
### Websites:
#https://spacy.io/models/en
#https://huggingface.co/spaces/presidio/presidio_demo
#https://microsoft.github.io/presidio/getting_started/
#https://microsoft.github.io/presidio/api-docs/api-docs.html#tag/Analyzer/paths/~1supportedentities/get


# # Not included entities as for https://microsoft.github.io/presidio/supported_entities/: ["DATE_TIME"]
# # How to set up new entity: https://microsoft.github.io/presidio/analyzer/adding_recognizers/
#
# # Set up the engine, loads the NLP module (spaCy model by default)
# # and other PII recognizers
# analyzer = AnalyzerEngine()
#
# # Call analyzer to get results
# results = analyzer.analyze(text=enquiry,
#                            entities=entities,
#                            language='en',
#                            score_threshold=0.5
#                            )
#
# print("Results: ", results)
#
# #Analyzer results are passed to the AnonymizerEngine for anonymization
# #find the different operators here: https://microsoft.github.io/presidio/anonymizer/adding_operators/
#
# anonymizer = AnonymizerEngine()
#
# anonymized_text = anonymizer.anonymize(text=enquiry, analyzer_results=results,
#                                        operators={"DEFAULT": OperatorConfig("replace")})
#
# print("Anonymized text: ", anonymized_text)
