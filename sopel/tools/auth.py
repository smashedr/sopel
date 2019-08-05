import datetime
import logging
import requests

logger = logging.getLogger('sopel')


def get_auth_token(bot):
    logger.info('get_token')
    logger.info(dir(bot.db))
    # get_channel_value
    return 'oauth:ylo0h7xpmn7r60zd3srlj5hr4n8k3i'


# def get_oauth_token(bot):
#     token = bot.db.get_channel_value(bot.config.core.channels[0], 'oauth2token') or {}
#     if not token:
#         logger.info('NO TOKEN FOUND: Initializing default token for bot {}'.format(bot.config.core.nick))
#         token = {
#             'refresh_token': bot.config.twitch.initial_refresh,
#             'iso_expire': datetime.datetime.now().isoformat(),
#         }
#     logger.debug(token['iso_expire'])
#     expiration = iso_to_dt(token['iso_expire'])
#     logger.debug(expiration)
#     if datetime.datetime.now() < expiration:
#         logger.debug('-- access token not expired --')
#         return token['access_token']
#
#     logger.debug('-- access token EXPIRED --')
#     try:
#         refresh = refresh_twitch_token(
#             bot.config.twitch.client_id, bot.config.twitch.client_secret, token['refresh_token']
#         )
#     except Exception as error:
#         logger.exception(error)
#         return None
#
#     expire_at = datetime.datetime.now() + datetime.timedelta(seconds=refresh['expires_in'])
#     logger.debug(expire_at)
#     token = {
#         'access_token': refresh['access_token'],
#         'refresh_token': refresh['refresh_token'],
#         'iso_expire': expire_at.isoformat(),
#     }
#     logger.debug(token)
#     bot.db.set_channel_value(bot.config.core.channels[0], 'oauth2token', token)
#     return token['access_token']
#
#
# def refresh_twitch_token(client_id, client_secret, refresh_token):
#     url = 'https://id.twitch.tv/oauth2/token'
#     data = {
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token,
#         'client_id': client_id,
#         'client_secret': client_secret,
#     }
#     r = requests.post(url, json=data, timeout=10)
#     logger.debug(r.content)
#     if r.ok:
#         return r.json()
#     else:
#         r.raise_for_status()
#
#
# def iso_to_dt(dt_str):
#     dt, _, us = dt_str.partition('.')
#     dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
#     return dt + datetime.timedelta(microseconds=int(us.rstrip('Z'), 10))
