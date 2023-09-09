# TODO couple these with story types.....by using a TUPLE?????
defaultStories = [
  "Pockets stop working worldwide",
  "Very hungry caterpillar escapes the zoo",
  "Local man discovers gold nugget in the river worth over $50",
  "Money is up 30%",
  "Uninspired group of friends has game create news story for them rather than make it themselves"
  "Scrappy-doo found dead in Miami"
]

prompts = {
    # GENERAL ---------------------------------------------------------------------------------
    # CRIME -----------------------------------------------------------------------------------
    "crime_intro_1": {
        "tags": ["introduction","crime"],
        "lines": [
            {
                "speaker": "host",
                "text": "I'm {host} {host_lastname} with Telimpropmtu news.",
            },
            {
                "speaker": "cohost",
                "text": "And I'm {cohost} {cohost_lastname}",
            },
            {
                "speaker": "host",
                "text": "Our leading story tonight, {main_story}. Here's what we know so far: {main_story_info}",
                "prompts": [
                    {
                        "id": "main_story",
                        "description": "Initial details about the story, {main_story}"
                    },
                    {
                        "id": "main_story_info",
                        "description": "Initial details about the story, {main_story}"
                    }
                ]
            },
            {
                "speaker": "cohost",
                "text": "That's right {@host}, We are also being told {!main_story_info_2}",
                "prompts": {
                    "id": "main_story_info2",
                    "description": "Details about the story, {main_story}. What we know so far: {main_story_info}."
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
                "propmts":  {
                    "id": "detective_info1",
                    "description": "Write a discovery for the detective to present. Context: 'Well, the situation is worse than we thought. My team has just discovered that (Your text here)."
                },
                
            },
            {
                "speaker": "host",
                "text": "Horrific."
            },
            {
                "speaker": "detective",
                "text": "It gets worse. In all my years as a detective never before have I seen {detective_info2}.",
                "prompts":   {
                    "id": "detective_info2",
                    "description": "Write a discovery for the detective to present. Context: 'It gets worse, in all my years as a detective never before have I seen (your text here)"
                },
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
                    "description": "The detective will present a note that was discovered at the scene. Write what the note says."
                }
            },
            {
                "speaker": "host",
                "text": "Detective, thank you for your time."
            }
        ],
    },
    "crime_conclusion_1": {
        "tags": ["conclusion"],
        "lines": [
            {
                "speaker": "HOST",
                "text": "Well, there you have it folks. A story like this you only see once in a lifetime. {!host_story_description} {@cohost} its an unbelievable story isn't it?",
                "prompts": [
                    {
                        "id": "host_story_description",
                        "description": "A few words for the closing remarks of the story\nContext: \"Well, there you have it folks. A story like this you only see once in a lifetime. (Your text here)\""
                    }
                ]
            },
            {
                "speaker": "COHOST",
                "text": "Well, it shouldn't be all that surprising given that {!cohost_statistic}.",
                "prompts": [
                    {
                        "id": "cohost_statistic",
                        "description": "A fake fact or statistic for the CoHost to present\nContext: \"Perhaps this story shouldn't be all that surprising given that (Your text here)\""
                    }
                ]
            },
            {
                "speaker": "HOST",
                "text": "Well folks, that's all the time we have for tonight. Goodbye."
            }
        ]
    },
    # POLITICS -----------------------------------------------------------------------------------
    "politics_intro_1": {
        "tags": ["introduction", "politics"],
        "lines": [
            {"speaker": "host", "text": "Good evening, I'm {host} {host_lastname} and this is Politics Today."},
            {"speaker": "cohost", "text": "And I'm {cohost} {cohost_lastname}. The political landscape is buzzing with activity!"},
            {
                "speaker": "host",
                "text": "Indeed, the latest development from the Capitol is {main_story}.",
                "prompts": {
                    "id": "main_story",
                    "description": "Main political event or development for the day."
                }
            }
        ],
    },
    "politics_segment_1": {
        "tags": ["segment", "politics"],
        "lines": [
            {"speaker": "host", "text": "We're joined by Senator {senator}."},
            {
                "speaker": "senator",
                "text": "Thank you for having me. It's crucial to address {senator_issue}.",
                "prompts": {
                    "id": "senator_issue",
                    "description": "Primary political issue Senator wants to discuss."
                }
            },
            {"speaker": "cohost", "text": "Senator, what are your thoughts on the opposition's stance?"},
            {
                "speaker": "senator",
                "text": "Well, it's a complex issue, but I believe {senator_response}.",
                "prompts": {
                    "id": "senator_response",
                    "description": "Senator's response or viewpoint on the issue at hand."
                }
            }
        ],
    },
    "politics_conclusion_1": {
        "tags": ["conclusion", "politics"],
        "lines": [
            {"speaker": "host", "text": "It's been an eventful day in the world of politics."},
            {"speaker": "cohost", "text": "Absolutely. Stay informed and we'll be back with more updates tomorrow."}
        ],
    },

    # SPORTS -----------------------------------------------------------------------------------------------------------

    "sports_intro_1": {
        "tags": ["introduction", "sports"],
        "lines": [
            {"speaker": "host", "text": "Welcome to Sports Night, I'm {host} {host_lastname}."},
            {"speaker": "cohost", "text": "And I'm {cohost} {cohost_lastname}. What a game we had last night!"},
            {
                "speaker": "host",
                "text": "Truly memorable! {main_sports_story}.",
                "prompts": {
                    "id": "main_sports_story",
                    "description": "Main highlight or event from the recent sports game or match."
                }
            }
        ],
    },
    "sports_segment_1": {
        "tags": ["segment", "sports"],
        "lines": [
            {"speaker": "host", "text": "Joining us now is {athlete_name}, the star player from last night's game."},
            {"speaker": "athlete", "text": "Thanks for having me! That was one of my best performances."},
            {"speaker": "cohost", "text": "Tell us about that incredible goal."},
            {
                "speaker": "athlete",
                "text": "It was a team effort, but when I saw the opening, I just went for it.",
                "prompts": {
                    "id": "athlete_goal_detail",
                    "description": "Details or circumstances surrounding the athlete's memorable goal or play."
                }
            }
        ],
    },
    "sports_conclusion_1": {
        "tags": ["conclusion", "sports"],
        "lines": [
            {"speaker": "host", "text": "What a day in sports history."},
            {"speaker": "cohost", "text": "Absolutely! We'll be back tomorrow with more highlights."}
        ],
    },
}