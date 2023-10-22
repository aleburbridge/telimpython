from enum import Enum

class Role(Enum):
    HOST = "host"
    COHOST = "cohost"
    GUEST_EXPERT = "guest expert"
    DETECTIVE = "detective"
    FIELD_REPORTER = "field reporter"
    WITNESS = "witness"
    POLITICIAN = "politician"
    SPORTS_REPORTER = "sports reporter"
    SPORTS_PLAYER = "sports player"
    CRIMINAL = "criminal"

last_names = {
    Role.HOST: ["Hosterson", "McHostly", "Hostdanews"],
    Role.COHOST: ["McCohost", "Reportsalot"],
    Role.GUEST_EXPERT: ["Expertson"],
    Role.DETECTIVE: ["Gumshoe"],
    Role.FIELD_REPORTER: ["Fieldsley", "Mansfield"],
    Role.WITNESS: ["Sawdathing"],
    Role.POLITICIAN: ["Kennedy"],
    Role.CRIMINAL: ["McGuilty"],
    Role.SPORTS_REPORTER: ["Kickaball"],
    Role.SPORTS_PLAYER: ["Runquick"]
}