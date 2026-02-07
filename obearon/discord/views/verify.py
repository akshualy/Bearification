"""
Verify view.
"""

import os
import random

import discord
from loguru import logger

from obearon.database import crud


class VerifyView(discord.ui.View):
    """
    Class for handling the verify view/button.
    """

    def __init__(self):
        """
        Initialize the persistent verify view.
        timeout has to be None in order for the button to not break over restarts.
        """
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Join as a friend", style=discord.ButtonStyle.blurple, custom_id="verify_view:join_as_friend"
    )
    async def on_join_as_friend_click(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        """
        Triggered when a user clicks the "Join as a friend" button.

        Args:
          _: Required button argument.
          interaction: The interaction of the user.
        """
        guild_role = await crud.get_friend_role(interaction.guild_id)
        if not guild_role:
            logger.warning(f"No friend role set for {interaction.guild_id}.")
            await interaction.response.send_message(
                content="The bot was not able to give you the friend role because it is not set. Let an admin know!",
                ephemeral=True,
            )
            return

        logger.info(f"Marking {interaction.user.display_name} ({interaction.user.id}) as friend.")
        try:
            await interaction.user.add_roles(interaction.guild.get_role(guild_role.friend_role_id))
        except discord.Forbidden:
            logger.warning(
                f"Was not allowed to change roles of {interaction.user.display_name} ({interaction.user.id})."
            )
            await interaction.response.send_message(
                content="The bot was not able to give you the friend role. Let an admin know!",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            content="Welcome to With Our Bear Hands, friend!",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Join as a clan member", style=discord.ButtonStyle.green, custom_id="verify_view:join_as_clan"
    )
    async def on_join_as_clan_click(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        """
        Triggered when a user clicks the "Join as a clan member" button.

        Args:
          _: Required button argument.
          interaction: The interaction of the user.
        """
        verification_code = random.randint(100_000, 999_999)
        existing_verification_code = await crud.create_verification(
            discord_guild_id=interaction.guild_id,
            discord_user_id=interaction.user.id,
            verification_code=verification_code,
        )
        if existing_verification_code:
            verification_code = existing_verification_code

        if not existing_verification_code:
            logger.info(
                f"Added {interaction.user.display_name} ({interaction.user.id}) "
                f"with verification code {verification_code}."
            )

        await interaction.response.send_message(
            content=(
                f"1. Go to <https://forums.warframe.com/messenger/compose/?to={os.environ["USER_ID"]}&title={verification_code}>.\n"
                f"2. Enter anything in the message part.\n"
                "3. Send the message and **wait up to 2 minutes**[.](https://i.imgur.com/caLFbWY.png)\n\n"
                "If you have any issues, send a message in <#1279139946480926872> or to <@1268317208409538632>!"
            ),
            ephemeral=True,
        )
