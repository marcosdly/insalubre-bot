import logging
import sys

from local.io import ProjectFolders
from constants import Constants

__all__ = ["command_response_logger", "whatsapp_sending_logger", "command_action_logger"]

# This module is meant to almost never change anyway, let it be like that for now...

command_response_logger = logging.Logger("command_response_logger")
whatsapp_sending_logger = logging.Logger("whatsapp_sending_logger")
command_action_logger = logging.Logger("command_action_logger")

formatter = logging.Formatter(fmt="%(levelname)s:%(funcName)s:%(lineno)s message=\"%(message)s\"")

if Constants.args.debug_log_stdout:
    stream = logging.StreamHandler(sys.stdout)
    command_action_logger.addHandler(stream)
    command_response_logger.addHandler(stream)
    whatsapp_sending_logger.addHandler(stream)
else:
    cmd_response_handler = logging.FileHandler(ProjectFolders.logs.joinpath("command-response.log"), mode="a", encoding="utf-8")
    cmd_response_handler.setFormatter(formatter)
    cmd_response_handler.setLevel(Constants.args.debug_log_lvl)

    cmd_action_handler = logging.FileHandler(ProjectFolders.logs.joinpath("command-action.log"), mode="a", encoding="utf-8")
    cmd_action_handler.setFormatter(formatter)
    cmd_action_handler.setLevel(Constants.args.debug_log_lvl)

    whatsapp_sending_handler = logging.FileHandler(ProjectFolders.logs.joinpath("whatsapp-sending.log"), mode="a", encoding="utf-8")
    whatsapp_sending_handler.setFormatter(formatter)
    whatsapp_sending_handler.setLevel(Constants.args.debug_log_lvl)

    command_response_logger.addHandler(cmd_response_handler)
    command_action_logger.addHandler(cmd_action_handler)
    whatsapp_sending_logger.addHandler(whatsapp_sending_handler)

