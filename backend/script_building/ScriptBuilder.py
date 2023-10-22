import random
from segments import get_segments_with_tags
class ScriptBuilder:
    def __init__(self, players, story_type, story):
        self.players = players
        self.story_type = story_type
        self.story = story
        self.script_segments = []
        self.roles = [player.role.lower() for player in players]

    # and segment not in self.script_segments
    
    def build(self):
        intro = random.choice(get_segments_with_tags(["introduction", self.story_type]), self.roles)
        if intro:
            self.script_segments.append(intro)

        middle_segments = get_segments_with_tags(["segment", self.story_type], self.roles)
        random.shuffle(middle_segments)
        for i in range(len(self.players) - 2):
            if middle_segments[i]:
                self.script_segments.append(middle_segments[i])

        conclusion = random.choice(get_segments_with_tags(["conclusion", self.story_type]), self.roles)
        if conclusion:
            self.script_segments.append(conclusion)

        return self.script_segments
    
    def extract_lines_with_prompts(self, script):
        lines_with_prompts = []
        for segment in script:
            for line in segment["lines"]:
                if "prompts" in line:
                    lines_with_prompts.append(line)
        return lines_with_prompts
    
    def fill_in_initial_script_details(self):
        roles_to_names = {player.role: player.name for player in self.players}
        roles_to_lastnames = {player.role: player.last_name for player in self.players}

        for segment in self.script_segments:
            for line in segment["lines"]:
                for role, name in roles_to_names.items():
                    line["text"] = line["text"].replace(f"{{{role}}}", name)
                    
                for role, lastname in roles_to_lastnames.items():
                    line["text"] = line["text"].replace(f"{{{role}_lastname}}", lastname)
                        
                line["text"] = line["text"].replace("{main_story}", self.story)
                    
        return self.script_segments
