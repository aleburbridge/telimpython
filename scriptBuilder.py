from prompts import prompts

class ScriptBuilder:
    def __init__(self, players, roles, storyType):
        self.roles = lobby_code

    def _add_intro(self):
        for key, value in prompts.items():
            if 'introduction' in value['tags'] and 'crime' in value['tags']:
                self.script.extend(value['lines'])
                break

    def _add_segments(self):
        segment_roles = [role for role in self.roles if role.lower() not in ['host', 'cohost']]
        available_segments = [segment for key, segment in prompts.items() if 'segment' in segment['tags'] and 'crime' in segment['tags']]
        
        for idx, role in enumerate(segment_roles):
            if idx < len(available_segments):
                self.script.extend(available_segments[idx]['lines'])
            else:
                break
    
    def _add_conclusion(self):
        for key, value in prompts.items():
            if 'conclusion' in value['tags']:
                self.script.extend(value['lines'])
                break
    
    def build(self):
        self._add_intro()
        self._add_segments()
        self._add_conclusion()
        return self.script