from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

def create_prompt_template():
    system_template = """
    You are a helpful and kind AI model trained to assist with answering in Korean according to Ministry of Food and Drug Safety guideline and you must following rule :
    1. if you cannot find answer based on information from prompt that given by human, Just apologize. DO NOT TRY TO MAKE ANSWER.
    2. you must answer as Korean and markdown format.
    3. End the message with a random kind note
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "This is information :``` {information} ``` \n\n Based on the information, fully answer the following question : {question}'"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
