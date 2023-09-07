# TODO couple these with story types.....by using a TUPLE?????
defaultStories = [
  "Pockets stop working worldwide",
  "Very hungry caterpillar escapes the zoo",
  "Local man discovers gold nugget in the river worth over $50",
  "Money is up 30%",
  "Group of x uncreative friends cant decide on a prompt and need a game to do it for them"
  "Scrappy-doo found dead in Miami"
]

prompts = {
    "Crime": {
        "Host": [
            {
                "part_of_story": "introduction",
                "context": "Describe the horrible crime",
                "instruction": "State facts and figures about the {crime}",
                "dependencies": []  # no dependencies
            },
            
        ],
        "Detective": [
            {
                "part_of_story": "middle",
                "context": "Share clues",
                "instruction": "Discuss the clues found at the {scene}",
                "dependencies": ["Host"]  # dependent on Host's answer
            },
            
        ],
    },
    "Politics": {
          "Host": [
            {
                "part_of_story": "introduction",
                "context": "",
                "instruction": "State facts and figures about the {crime}",
                "dependencies": []  # no dependencies
            },
            
        ],
    },
    "Sports": {

    },
    "Other": {

    }
}
