import random
from segments import segments

class ScriptBuilder:
    def __init__(self, players, story_type, story):
        self.players = players
        self.story_type = story_type
        self.story = story
        self.script_segments = []
        self.roles = [player.role.lower() for player in players]
        print("In script builder. Roles are")
        print(self.roles)

    def _get_segment_with_tags(self, required_tags):
        suitable_segments = [
            segment for segment in segments.values() 
            if all(tag in segment["tags"] for tag in required_tags) and
            all(line["speaker"] in self.roles for line in segment["lines"]) and
            segment not in self.script_segments
        ]
        return random.choice(suitable_segments) if suitable_segments else None
    
    def build(self):
        intro = self._get_segment_with_tags(["introduction", self.story_type])
        if intro:
            print("Intro is")
            print(intro)
            self.script_segments.append(intro)

        for _ in range(len(self.players) - 2):
            segment = self._get_segment_with_tags(["segment", self.story_type])
            if segment:
                print("segment is")
                print(segment)
                self.script_segments.append(segment)
            else:
                print("No segment :(")

        conclusion = self._get_segment_with_tags(["conclusion", self.story_type])
        if conclusion:
            self.script_segments.append(conclusion)

        return self.script_segments
    
    def extract_prompts(self, script):
        prompts = []
        for segment in script:
            for line in segment["lines"]:
                if "prompts" in line:
                    prompts.append(line)
        return prompts
    
    def fill_in_initial_script_details(self):
        roles_to_names = {player.role: player.name for player in self.players}
        roles_to_lastnames = {player.role: player.last_name for player in self.players}
        print("lastnames:")
        print(roles_to_lastnames)
        for segment in self.script_segments:
            for line in segment["lines"]:
                for role, name in roles_to_names.items():
                    line["text"] = line["text"].replace(f"{{{role}}}", name)
                    
                for role, lastname in roles_to_lastnames.items():
                    line["text"] = line["text"].replace(f"{{{role}_lastname}}", lastname)
                        
                line["text"] = line["text"].replace("{main_story}", self.story)
                    
        return self.script_segments
