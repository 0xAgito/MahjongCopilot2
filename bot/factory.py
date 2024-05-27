""" Bot factory"""
from common.settings import Settings
from common.utils import Folder, sub_file
from .bot import Bot, GameMode
from .local.bot_local import BotMortalLocal
from .mjapi.bot_mjapi import BotMjapi
from .akagiot.bot_akagiot import BotAkagiOt


MODEL_TYPE_STRINGS = ["Local", "AkagiOT", "MJAPI"]
OT2_MODEL_PATH = "./mjai/bot_3p/model.pth"


def get_bot(settings:Settings) -> Bot:
    """ create the Bot instance based on settings"""
    
    match settings.model_type:
        case "Local":
            if settings.enable_ot2_for_3p:
                model_files:dict = {
                    GameMode.MJ4P: sub_file(Folder.MODEL, settings.model_file),
                    GameMode.MJ3P: OT2_MODEL_PATH
                }
            else:
                model_files:dict = {
                    GameMode.MJ4P: sub_file(Folder.MODEL, settings.model_file),
                    GameMode.MJ3P: sub_file(Folder.MODEL, settings.model_file_3p)
                }
            bot = BotMortalLocal(model_files)
        case "AkagiOT":
            bot = BotAkagiOt(settings.akagi_ot_url, settings.akagi_ot_apikey)
        case "MJAPI":
            bot = BotMjapi(settings)
        case _:
            raise ValueError(f"Unknown model type: {settings.model_type}")

    return bot


