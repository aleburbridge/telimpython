import random
from segments import segments

class ScriptBuilder:
    def __init__(self, players, story_type, roles):
        self.players = players
        self.story_type = story_type
        self.roles = roles

    def _get_segment_with_tags(self, required_tags):
        suitable_segments = [
            segment for segment in segments.values() 
            if all(tag in segment["tags"] for tag in required_tags) and
            all(line["speaker"] in self.roles for line in segment["lines"])
        ]
        return random.choice(suitable_segments) if suitable_segments else None
    
    def build(self):
        script_segments = []

        intro = self._get_segment_with_tags(["introduction"] + self.story_type)
        if intro:
            script_segments.append(intro)

        for _ in range(len(self.players) - 2):
            segment = self._get_segment_with_tags(["segment"] + self.story_type)
            if segment:
                script_segments.append(segment)

        conclusion = self._get_segment_with_tags(["conclusion"] + self.story_type)
        if conclusion:
            script_segments.append(conclusion)

        return script_segments

