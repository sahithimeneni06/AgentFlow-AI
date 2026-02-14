from llm.llm import ask_llm
import re

class StudyAgentV3:

    def __init__(self):
        self.tools = {
            'calculator': self.calculator,
            'word_counter': self.word_counter
        }

    def calculator(self, expression):
        try:
            return eval(expression)
        except:
            return 'Invalid Math'

    def word_counter(self, text):
        return len(text.split())

    def think(self, user_ip):

        prompt = f"""
You are an agent that selects a tool.

Available actions:
calculator → for math
word_counter → for counting words
respond → for normal answers

Return ONLY:

ACTION: <action>
INPUT: <input>

Examples:

Input: what is 8*7
ACTION: calculator
INPUT: 8*7

Input: count words in i am good
ACTION: word_counter
INPUT: i am good

Input: explain transformers
ACTION: respond
INPUT: explain transformers

Now decide:

Input: {user_ip}
ACTION:
"""

        return ask_llm(prompt)

    def parse(self, llm_output):

        if not isinstance(llm_output, str):
            return "respond", str(llm_output)

        llm_output = llm_output.strip().lower()

        if llm_output in self.tools:
            return llm_output, llm_output

        action_match = re.search(r"ACTION:\s*(\w+)", llm_output, re.IGNORECASE)
        input_match = re.search(r"INPUT:\s*(.+)", llm_output, re.IGNORECASE | re.DOTALL)

        if action_match and input_match:
            action = action_match.group(1).strip().lower()
            tool_input = input_match.group(1).strip()
            return action, tool_input

        return "respond", llm_output

    def run(self, user_ip):
        if re.search(r"[0-9]+\s*[\+\-\*/]\s*[0-9]+", user_ip):
            expr = re.sub(r"[^0-9+\-*/().]", "", user_ip)
            return self.calculator(expr)

        if user_ip.lower().startswith("count words"):
            text = user_ip.replace("count words", "")
            return self.word_counter(text)
        decision = self.think(user_ip)
        print("LLM OUTPUT:\n", decision)

        action, tool_ip = self.parse(decision)
        if action == "calculator":
            tool_ip = re.sub(r"[^0-9+\-*/().]", "", tool_ip)
            return self.calculator(tool_ip)

        if action == "word_counter":
            return self.word_counter(tool_ip)
        answer_prompt = f"""
    You are a helpful study assistant.

    Question: {user_ip}
    Answer clearly:
    """

        return ask_llm(answer_prompt)


# agent = StudyAgentV3()

# while True:
#     user = input('You (Type "exit" or "q" or "quit" to exit) : ')
#     if user in ['exit', 'q', 'quit', 'bye']:
#         print('GoodBye...')
#         break
#     print('Agent : ', agent.run(user))