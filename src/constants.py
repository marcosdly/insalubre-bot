import argparse
from typing import NamedTuple
from logging import getLevelNamesMapping

__all__ = ["Constants"]

class Suffixes(NamedTuple):
    sudo: str = "+eu_sou_estupido"
    insecure: str = "+eu_sou_inseguro"

class Constants:
    args: argparse.Namespace
    suffixes: Suffixes

    __initted: bool = False

    @classmethod
    def __parse_args(cls) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            prog="insalubre-bot",
            description="Discord bot that tells my friends when one of them are online.",
            add_help=True,
            allow_abbrev=True,
            exit_on_error=True,
        )

        parser.add_argument("--debug",help="Log to stdin instead of warning friends", default=False, dest="debug", action="store_true")
        parser.add_argument("--log-stdout", help="Send debug logs to stdout", default=False, dest="debug_log_stdout", action="store_true")
        parser.add_argument("--log-level", type=str, help="Debug log level", default="INFO", choices=getLevelNamesMapping().keys(), dest="debug_log_lvl")
        
        return parser.parse_args()

    @classmethod
    def initialize(cls):
        # Way more explicit to write than __init__
        if cls.__initted:
            raise SyntaxError("The Constants class cannot be initialized twice.")

        cls.args = cls.__parse_args()
        cls.suffixes = Suffixes()

        cls.__initted = True

