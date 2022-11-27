import os
import random
import sys
from configparser import ConfigParser

__config = ConfigParser()

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    abs_pth = os.path.abspath(sys.argv[0])
    application_path = os.path.dirname(abs_pth)

__config.read(os.path.join(application_path, "config.ini"))


TOKEN = __config["DISCORD"]["TOKEN"]
GUILD_ID = int(__config["DISCORD"]["GUILD_ID"])
CHANNEL_ID = int(__config["DISCORD"]["CHANNEL_ID"])

TITLE = __config["EMBED"]["TITLE"]
DESCRIPTION = __config["EMBED"]["DESCRIPTION"]
INLINE = __config["EMBED"].getboolean("INLINE", fallback=False)
COLOR = int(__config["EMBED"]["COLOR"], 16)
THUMBNAIL = __config["EMBED"]["THUMBNAIL"]
FOOTER = __config["EMBED"]["FOOTER"]

EFFECTS_COUNT = int(__config["GAME"]["EFFECTS_COUNT"])
EFFECTS_HISTORY = int(__config["GAME"]["EFFECTS_HISTORY"])
VOITING_TIME = float(__config["GAME"]["VOITING_TIME"])

AUGS = [aug.replace(" ", "") for aug in __config["GAME"]["AUGS"] if aug]
AMMO = [ammo.replace(" ", "") for ammo in __config["GAME"]["AMMO"] if ammo]

HOST = __config["SERVER"]["HOST"]
PORT = int(__config["SERVER"]["PORT"])

EFFECTS = []
__effects = __config["EFFECTS"]
for key, value in __effects.items():
    EFFECTS.extend((key, None) for _ in range(int(value)))

__give_health = __config["give_health"]
__give_energy = __config["give_energy"]
__give_skillpoints = __config["give_skillpoints"]
__remove_skillpoints = __config["remove_skillpoints"]
__add_credits = __config["add_credits"]
__remove_credits = __config["remove_credits"]
EFFECTS.extend(("give_health", [str(random.randint(__give_health.getint(
    "min"), __give_health.getint("max"))),]) for _ in range(1, __give_health.getint("count") + 1))
EFFECTS.extend(("give_energy", [str(random.randint(__give_energy.getint(
    "min"), __give_energy.getint("max"))),]) for _ in range(1, __give_energy.getint("count") + 1))
EFFECTS.extend(("give_skillpoints", [str(random.randint(__give_skillpoints.getint(
    "min"), __give_skillpoints.getint("max"))),]) for _ in range(1, __give_skillpoints.getint("count") + 1))
EFFECTS.extend(("remove_skillpoints", [str(random.randint(__remove_skillpoints.getint(
    "min"), __remove_skillpoints.getint("max"))),]) for _ in range(1, __remove_skillpoints.getint("count") + 1))
EFFECTS.extend(("add_credits", [str(random.randint(__add_credits.getint(
    "min"), __add_credits.getint("max"))),]) for _ in range(1, __add_credits.getint("count") + 1))
EFFECTS.extend(("remove_credits", [str(random.randint(__remove_credits.getint(
    "min"), __remove_credits.getint("max"))),]) for _ in range(1, __remove_credits.getint("count") + 1))

print("Loaded Config")
print("------------------")
