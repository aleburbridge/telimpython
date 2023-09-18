defaultStories = [
  "Pockets stop working worldwide",
  "Very hungry caterpillar escapes the zoo",
  "Local man discovers gold nugget in the river worth over $50",
  "Money is up 30%",
  "Uninspired group of friends has game create news story for them rather than make it themselves"
  "Scrappy-doo found dead in Miami"
]

segments = {
    # GENERAL ---------------------------------------------------------------------------------
    
    # CRIME -----------------------------------------------------------------------------------
    "crime_intro_1": {
        "tags": ["introduction", "crime"],
        "lines": [
            {"speaker": "host", "text": "I'm {host} {host_lastname} with Telimpropmtu news."},

            {"speaker": "cohost", "text": "And I'm {cohost} {cohost_lastname}"},

            {
                "speaker": "host",
                "text": "Our leading story tonight, {main_story}. Here's what we know so far: {main_story_info}",
                "prompts": {
                    "id": "main_story",
                    "description": "Initial details about the story."
                }
            },

            {
                "speaker": "host",
                "text": "{main_story_info}",
                "prompts": {
                    "id": "main_story_info",
                    "description": "Details about the leading story."
                }
            },

            {
                "speaker": "cohost",
                "text": "That's right {@host}, We are also being told {main_story_info_2}",
                "prompts": {
                    "id": "main_story_info_2",
                    "description": "More details about the story."
                }
            }
        ],
    },
    "crime_segment_1": {
        "tags": ["segment", "crime"],
        "lines": [
            {
                "speaker": "host",
                "text": "This just in, I'm getting word that we've managed to get an exclusive interview with Detective {detective} Gumshoe who is live on the scene. Detective, what can you share with us?"
            },
            {
                "speaker": "detective",
                "text": "Well, the situation is worse than we thought, my team has just discovered that {detective_info1}.",
                "prompts": {
                    "id": "detective_info1",
                    "description": "Write a discovery for the detective to present."
                }
            },
            {"speaker": "host", "text": "Horrific."},
            {
                "speaker": "detective",
                "text": "It gets worse. In all my years as a detective never before have I seen {detective_info2}.",
                "prompts": {
                    "id": "detective_info2",
                    "description": "Write a discovery for the detective to present."
                }
            },
            {
                "speaker": "cohost",
                "text": "Well detective, do you have any clues as to why this happened?"
            },
            {
                "speaker": "detective",
                "text": "Indeed I do. A note was discovered at the scene of the incident, it reads: {detective_note}.",
                "prompts": {
                    "id": "detective_note",
                    "description": "The detective will present a note that was discovered at the scene."
                }
            },
            {"speaker": "host", "text": "Detective, thank you for your time."}
        ],
    },
    "crime_conclusion_1": {
        "tags": ["conclusion", "crime"],
        "lines": [
            {
                "speaker": "host",
                "text": "Well, there you have it folks. A story like this you only see once in a lifetime. {host_story_description} {cohost}, its an unbelievable story isn't it?",
                "prompts": {
                    "id": "host_story_description",
                    "description": "A few words for the closing remarks of the story."
                }
            },
            {
                "speaker": "cohost",
                "text": "Well, it shouldn't be all that surprising given that {cohost_statistic}.",
                "prompts": {
                    "id": "cohost_statistic",
                    "description": "A fake fact or statistic for the CoHost to present."
                }
            },
            {"speaker": "host", "text": "Well folks, that's all the time we have for tonight. Goodbye."}
        ]
    },
}