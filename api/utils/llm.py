from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

class Chain:
    def __init__(self) -> None:
        pass

    def create(chat_prompt, info, question):
        try:
            return llm(chat_prompt.format_prompt(information= info, question= question).to_messages())
        except SystemError as e:
            print(e)
