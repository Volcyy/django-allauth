import requests

from allauth.socialaccount.providers.discord.provider import DiscordProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class DiscordOAuth2Adapter(OAuth2Adapter):
    provider_id = DiscordProvider.id
    access_token_url = 'https://discordapp.com/api/oauth2/token'
    authorize_url = 'https://discordapp.com/api/oauth2/authorize'
    guilds_url = 'https://discordapp.com/api/users/@me/guilds'
    profile_url = 'https://discordapp.com/api/users/@me'

    def complete_login(self, request, app, token, **kwargs):
        headers = {
            'Authorization': 'Bearer {0}'.format(token.token),
            'Content-Type': 'application/json',
        }
        guild_data = requests.get(self.guilds_url, headers=headers).json()
        profile_data = requests.get(self.profile_url, headers=headers).json()

        extra_data = {
            **profile_data,
            'guilds': guild_data
        }

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(DiscordOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DiscordOAuth2Adapter)
