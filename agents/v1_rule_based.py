import re

class StudyAgentV1:
    def think(self, user_ip):
        if re.fullmatch(r"[0-9+\-*/().\s]+", user_ip):
            return {'action':'calc', 'input':user_ip}
        math_match = re.findall(r"[0-9+\-*/().]+", user_ip)
        math_exp = ''.join(math_match)
        if len(math_exp)>2:
            return {'action':'calc', 'input':math_exp}
        count_rep = ['count words', 'count words in', 'COUNT WORDS', 'Count Words', 'cnt words', 'cnt words in']
        for w in count_rep:
            if w in user_ip:
                text = user_ip.replace(w, '')
                return {'action':'word_counter', 'input': text}
        return {'action': 'respond', 'input':user_ip}

    def act(self, decision):
        if decision['action']=='calc':
            try:
                return eval(decision['input'])
            except:
                return 'Invalid Math'
        if decision['action']=='word_counter':
            return len(decision['input'].split())
        return 'Iam a rule based Agent'
    def run(self, user_ip):
        decision = self.think(user_ip)
        print('Thought : ', decision)
        res = self.act(decision)
        return res

# agent = StudyAgentV1()

# while True:
#     user = input('You : ')
#     print('Agent : ', agent.run(user))