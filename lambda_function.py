import random
import time

"""
Session attributes will have the following values:
    startGame : start the game
    startTime : the time the quiz starts
    endTime : the time the quiz ends
    question : the current question the user must ask
    score : the number of questions answered

"""

attributes={'startGame' : False, 'startTime': 0, 'endTime': 0, 'question' : None, 'score' : 0}

"""
>Add in StartIntent to take in slot for "Start the game" to initiate the start question 
>Have it insert AnswerIntent
>Test mine and Jake's code with his integrated 
>Add in replayability
"""
#---------------------------------QUESTION HELPER METHODS---------------------------------#
#Helper method to create a question
def generate_question():
    number1 = random.randint(1,12)
    number2 = random.randint(1,12)

    product = number1*number2

    #if operator = 0, multiplication
    #if operator = 1, division
    operator = random.randint(0,1)

    #format is number 1, number 2, operator, answer
    #EX: (2,5,0,10) => 2*5=10
    #EX: (10,2,1,5) => 10/2=5
    if(operator == 0):
        return number1,number2,"times",product
    else:
        return product,number1,"divided by",number2

#say a question
def speech_question(question):
    return "{} {} {}".format(question[0],question[2],question[1])

#Starts the quiz
def start_quiz(intent, session):
    card_title = intent["name"]
    reprompt_text = ""
    should_end_session = False
    
    session_attributes = {}
    
    session_attributes['startGame'] = True
    session_attributes['startTime'] = time.time()
    session_attributes['question'] = generate_question()
    session_attributes['score']  = 0
    
    question = speech_question(session_attributes['question'])
    
    #print(session_attributes[startGame], session_attributes[startTime])
    speech_output = "The game will begin in 3, 2, 1. Go, " + question

    return build_response(session_attributes, build_speechlet_response(card_title, 
        speech_output, 
        reprompt_text, 
        should_end_session))

#Helper method to give the user a question, have them answer it through AnswerIntent
def answer_question(intent, session):
    card_title = intent["name"]
    session_attributes = session.get('attributes',{})
    speech_output = ""
    reprompt_text = ""
    should_end_session = False

    num_of_questions = 10

    answer = int(intent['slots']['answer']['value'])

    #if game hasn't started yet
    if session_attributes.get('startGame') == True:
        
        print(type(answer))
        if(answer == None):
            reprompt_text="Sorry, I didn't get that."
        elif(type(answer) == int and answer == session_attributes.get('question')[3]):
            speech_output = ("Correct ")
            session_attributes['score'] = session_attributes.get('score') + 1
            session_attributes['question'] = generate_question()
            speech_output += speech_question(session_attributes['question'])
        else:
            speech_output="Sorry, try again"
            speech_output += speech_question(session_attributes['question'])
            
        #if score is 10, stop the game
        if(session_attributes.get('score') >= num_of_questions):
            session_attributes['endTime'] = time.time()
            print(session_attributes['endTime'],session_attributes.get('startTime'), session_attributes.get('startGame'))
            speech_output = "You have reached the end of the 10 questions. " \
                            "Your score is %.2f seconds. Try to beat your score." \
                            "Thank you for playing. " % (session_attributes.get('endTime') - session_attributes.get('startTime'))
            should_end_session = True
    else:
        speech_output = "The game has not started yet. Say start the game when you are ready."
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# Creates the responses that Alexa uses
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

# =================================CUSTOM====================================

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Quick Maths. " \
                    "The following test will test your multiplication and division skills, " \
                    "You will be asked to answer 10 questions as fast as possible, Say, start the game to begin."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I didn't catch that. Say start the game to begin."

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
# =========================================================================

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
    # Dispatch to your skill's launch
    return get_welcome_response()

 
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # THE MIDDLE MAN
    if intent_name == "StartIntent":
        return start_quiz(intent,session)
    elif intent_name == "AnswerIntent":
        return answer_question(intent, session)
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

# =============================================================================

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
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
