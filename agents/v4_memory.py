from llm.llm import ask_llm

class StudyAgentV4:
    def __init__(self):
        self.memory = []
    
    def run(self, user_ip):
        history = '\n'.join(self.memory[-5:])
        prompt = f"""
You are a helpful study assistant.

Use simple and correct explanations.
Do not repeat words.
If the question is a follow-up, use the conversation context.

Conversation:
{history}

User: {user_ip}
Answer clearly in 3–4 sentences:
"""

        ans = ask_llm(prompt)
        self.memory.append(f"User: {user_ip}")
        self.memory.append(f"Agent: {ans}")
        return ans
# math_agent = StudyAgentV2()
# agent = StudentAgent4()
# while True:
#     user = input('You : ')
#     if user in ['q', 'quit', 'exit', 'bye']:
#         print('GoodBye...')
#         break
#     exp = math_agent.extract_math(user)
#     if exp:
#         print('Agent : ', eval(exp))
#         break
#     if user.lower().startswith('count words'):
#         text = user.replace('count words', '')
#         print('Agent : ', len(text.split()))
#         continue

#     print('Agent : ', agent.run(user))
