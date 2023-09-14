import logging
import re
import uuid
from abc import abstractmethod
from typing import List, Optional, Type

import requests
from langchain.agents import Tool, AgentExecutor
from langchain.memory.chat_memory import BaseChatMemory
from pydantic import Field
from steamship import Block
from steamship.agents.mixins.transports.steamship_widget import SteamshipWidgetTransport
from steamship.agents.schema import (
    AgentContext,
    Metadata,
    Agent,
)
from steamship.agents.service.agent_service import AgentService
from steamship.cli.cli import cli
from steamship.invocable import post, Config
from steamship.utils.kv_store import KeyValueStore

class TelegramTransportConfig(Config):
    bot_token: Optional[str] = Field(
        "6465986315:AAEYnwGSsx1lrVqYKtHF9kD6iPzDAq3JYws",
        description="Your telegram bot token.\nLearn how to create one here: "
        "https://github.com/steamship-packages/langchain-agent-production-starter/blob/main/docs/register-telegram-bot.md",
    )
    payment_provider_token: Optional[str] = Field(
        "350862534:LIVE:YzM1N2I4YmFmNjVj", description="Optional Payment provider token, obtained via @BotFather"
    )
    n_free_messages: Optional[int] = Field(
        2, description="Number of free messages assigned to new users."
    )
    api_base: str = Field(
        "https://api.telegram.org/bot", description="The root API for Telegram"
    )