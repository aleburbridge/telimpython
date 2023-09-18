import unittest
from ScriptBuilder import ScriptBuilder

from app import Player

class TestScriptBuilder(unittest.TestCase):
    
    def setUp(self):
        self.players = [
            Player(name='Alice', role='host'),
            Player(name='Bob', role='cohost'),
            Player(name='Charlie', role='detective')
        ]
        self.story_type = ['crime']
        self.story = "A mysterious theft in downtown Seattle."  
    
    def test_build(self):
        builder = ScriptBuilder(self.players, self.story_type, self.story)
        script_segments = builder.build()
        print(script_segments)
        
        self.assertEqual(len(script_segments), len(self.players))

        roles = [player.role for player in self.players] 
        for segment in script_segments:
            for line in segment['lines']:
                self.assertIn(line['speaker'], roles)

if __name__ == '__main__':
    unittest.main()
