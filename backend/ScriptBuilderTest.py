import unittest
from ScriptBuilder import ScriptBuilder

class TestScriptBuilder(unittest.TestCase):
    
    def setUp(self):
        self.players = ['Alice', 'Bob', 'Charlie']
        self.roles = ['host', 'cohost', 'detective']
        self.story_type = ['crime']
    
    def test_build(self):
        builder = ScriptBuilder(self.players, self.story_type, self.roles)
        script_segments = builder.build()
        print(script_segments)
        
        self.assertEqual(len(script_segments), len(self.players))

        for segment in script_segments:
            for line in segment['lines']:
                self.assertIn(line['speaker'], self.roles)

if __name__ == '__main__':
    unittest.main()
