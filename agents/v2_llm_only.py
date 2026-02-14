from llm.llm import ask_llm
import re

class StudyAgentV2:
    def is_math(self, text):
        return re.fullmatch(r"[0-9+\-*/().\s]+", text)
    def extract_math(self, text):
        parts = re.findall(r"[0-9+\-*/().]+", text)
        expr = ''.join(parts)

        if any(op in expr for op in "+-*/") and len(expr) > 2:
            return expr
        return None

    def run(self, user_ip):
        if user_ip.lower().startswith("count words"):
            text = user_ip.replace("count words", "")
            return len(text.split())

        if self.is_math(user_ip):
            return eval(user_ip)
        expr = self.extract_math(user_ip)
        if expr:
            return eval(expr)
        prompt = f"""
You are a helpful study assistant.

Answer the question clearly and correctly.
Do not repeat sentences.
If a word limit is given, follow it.

Question: {user_ip}

Answer:
"""


        return ask_llm(prompt)

# agent = StudyAgentV2()

# while True:
#     user = input('You (Type "exit" or "q" or "quit" to exit) : ')
#     if user in ['exit', 'q', 'quit', 'bye']:
#         print('GoodBye...')
#         break
#     print('Agent : ', agent.run(user))