import logging
import sys

logger = logging.getLogger('soppel')

logger.info('tokenauth')


def get_auth_token(bot):
    logger.info('get_token')
    print('get_token')
    logger.info(dir(bot))
    # sys.exit(0)
    return 'oauth:ylo0h7xpmn7r60zd3srlj5hr4n8k3i'
