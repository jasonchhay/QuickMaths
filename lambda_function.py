# Creates the responses that Alexa uses================================================
import time
#Add the timer to time the user throughout the quiz

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

#==============================Greeting=And=Other=Shit==================================

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Quick Maths. " \
                    "The following test will test your multiplication and division skills, " \
                    "There are twenty questions that will be asked, Are you ready to play?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "The following test will test your multiplication and division skills, " \
                    "There are twenty questions that will be asked, Are you ready to play?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing Quick Maths. " \
                    ". Come play again soon!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def set_question_in_session(intent, session, question):
    card_title = intent['name']
    session_attributes = {
    should_end_session = False
# >>>> Set Intent Name below (I guessed lol)
     if 'Question' in intent['slots']:
        result = intent['slots']['Question']['value']
        session_attributes = result(question) #here too
        speech_output = #question var here
        reprompt_text = #not sure what to put
    else:
        speech_output = "I'm not sure what you just said. " \
                        "Please try again."
        reprompt_text = "I'm not sure what you just said. " \
                        "Please restate your answer,"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_result_from_session(intent, session, question): #add question count to this?
    session_attributes = {}
    reprompt_text = None

    if questionCount <= 20
        speech_output = question #add potential sound effect based on correct/wrong
        should_end_session = False
        questionCount = questionCount + 1
    else:
        speech_output = "You have completed the quiz!" \
                        ". Your total score was." + score + "out of " questionCount.format(result)
        should_end_session = True #Add replayability feature?

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

#=============================================Calling=On=Intents=========================================

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

     if intent_name == "AdditionIntent": #Replace all intents and add as necessary in this bit
        return addition(intent, session)
    elif intent_name == "SubtractingIntent":
        return subtract(intent, session)
    elif intent_name == "MultiplyIntent":
        return multiply(intent, session)
    elif intent_name == "DivisionIntent":
        return divide(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# ====================================Lambda=Function============================================

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

#======================================Add=All=Extra=Methods=Below==================================


