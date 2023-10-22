from script_building.roles import Role
from enum import Enum

class StoryType(Enum):
    CRIME = "crime"
    POLITICS = "politics"
    SPORTS = "sports"
    OTHER = "other"


story_type_to_roles = {
    StoryType.CRIME: [Role.HOST, Role.COHOST, Role.DETECTIVE],
    StoryType.POLITICS: [Role.HOST, Role.COHOST, Role.GUEST_EXPERT, Role.FIELD_REPORTER, Role.WITNESS, Role.POLITICIAN],
    StoryType.SPORTS: [Role.HOST, Role.COHOST, Role.SPORTS_REPORTER, Role.SPORTS_PLAYER],
    StoryType.OTHER: [Role.HOST, Role.COHOST, Role.GUEST_EXPERT, Role.DETECTIVE, Role.FIELD_REPORTER, Role.WITNESS, Role.POLITICIAN, Role.CRIMINAL],
}
