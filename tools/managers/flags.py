from discord.ext.commands import Converter, BasicFlags
from typing import Optional


class ScriptFlags(BasicFlags):
    not_strict: bool = False
