import datetime
import logging
import os
import requests

logger = logging.getLogger('sopel')


class TwitchAuth(object):
    @classmethod
    def get_bot_token(cls, bot, oauth=False):
        token = cls._get_oauth_token(bot, 'bot_token', 'bot_refresh')
        if oauth:
            return 'oauth:{}'.format(token)
        else:
            return token

    @classmethod
    def get_owner_token(cls, bot, oauth=False):
        token = cls._get_oauth_token(bot, 'owner_token', 'owner_refresh')
        if oauth:
            return 'oauth:{}'.format(token)
        else:
            return token

    @classmethod
    def _get_oauth_token(cls, bot, db_key, refresh_key):
        token = bot.db.get_channel_value(bot.config.twitch.owner_id, db_key) or {}
        if not token:
            logger.info('NO TOKEN FOUND: Initializing default token for: {}'.format(db_key))
            token = {
                'refresh_token': getattr(bot.config.twitch, refresh_key),
                'iso_expire': datetime.datetime.now().isoformat(),
            }

        if datetime.datetime.now() < cls.iso_to_dt(token['iso_expire']):
            logger.debug('-- access token valid --')
            return token['access_token']

        logger.debug('-- access token EXPIRED --')
        refresh = cls.refresh_twitch_token(
            os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'], token['refresh_token']
        )
        expire_at = datetime.datetime.now() + datetime.timedelta(seconds=refresh['expires_in'])
        token = {
            'access_token': refresh['access_token'],
            'refresh_token': refresh['refresh_token'],
            'iso_expire': expire_at.isoformat(),
        }
        logger.debug(token)
        bot.db.set_channel_value(bot.config.twitch.channel, db_key, token)
        return token['access_token']

    @staticmethod
    def refresh_twitch_token(client_id, client_secret, refresh_token):
        url = 'https://id.twitch.tv/oauth2/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        r = requests.post(url, json=data, timeout=10)
        logger.debug(r.content)
        if r.ok:
            return r.json()
        else:
            r.raise_for_status()

    @staticmethod
    def iso_to_dt(dt_str):
        dt, _, us = dt_str.partition('.')
        dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
        return dt + datetime.timedelta(microseconds=int(us.rstrip('Z'), 10))
