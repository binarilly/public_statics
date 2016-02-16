# coding=utf-8

__author__ = 'user'


class ConfigException(Exception):
    """
    Deployment job config exception。
    """
    pass


class ConfigManager(object):
    """
    Configuration management service。
    """
    _configs = None

    def __init__(self, env):
        super(ConfigManager, self).__init__()
        if not env:
            raise ConfigException(u'Evn configuration is required for deploy project.')
        # load setting module
        try:
            env_settings_module = __import__('config.%s' % env)
        except ImportError as e:
            raise ConfigException(u'No env deployment settings has been found. Refer fail reason: %s.' % e)
        if env in dir(env_settings_module):
            env_settings_module = getattr(env_settings_module, env)
            self._configs = {}
            for key in dir(env_settings_module):
                if not key.startswith('__'):
                    self._configs.update(
                        {key: getattr(env_settings_module, key)}
                    )
            self._configs.update({"env": env})

    def get(self, key, default=None):
        if self._configs and key in self._configs:
            return self._configs.get(key, default)
        return default

    def __setattr__(self, key, value):
        if '_configs' != key:
            raise NotImplementedError
        super(ConfigManager, self).__setattr__(key, value)
