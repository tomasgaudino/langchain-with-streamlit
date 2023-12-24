import pickle

from langchain.schema import HumanMessage
from langchain.memory import ConversationBufferMemory


class ConversationMemory:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.memory = self._get_langchain_memory()

    def _get_memory_summary(self):
        pass

    def _get_langchain_memory(self):
        if not self.file_path:
            return ConversationBufferMemory()
        else:
            try:
                with open(self.file_path, "rb") as f:
                    conversation_memory = pickle.load(f)
                return conversation_memory.memory
            except FileNotFoundError:
                print(f"There was an error loading the file {self.file_path}")
                return ConversationBufferMemory()

    @property
    def session_state_messages(self):
        return self._format_memory_to_session_state()

    def _format_memory_to_session_state(self):
        parsed_messages = [{'user' if isinstance(message, HumanMessage) else 'assistant': message.content} for message
                           in self.memory.chat_memory.messages]
        session_state_messages = [{'role': list(message.keys())[0], 'content': list(message.values())[0]} for message
                                  in parsed_messages]
        return session_state_messages

    @property
    def chat_id(self):
        return self._get_chat_id()

    def _get_chat_id(self):
        return self.file_path.split('/')[-1][:-4]
