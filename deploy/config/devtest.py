import os

__author__ = 'user'


location = lambda x: os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'), x)

# ============================ LOCAL BUILDING SETTINGS ============================ #
PROJECT_NAME = 'public_static'
PROJECT_ROOT_PATH = location('.')
SOURCE_PATH = location('statics')
SOURCE_OUTPUT_PATH = 'statics'
LOCAL_OUTPUT_PATH = location('out')
CONFIG_PATH = 'deploy/config/env/%s'
CONFIG_OUTPUT_PATH = 'config'
# ============================ LOCAL BUILDING SETTINGS ============================ #

# ============================ REMOTE BUILDING SETTINGS ============================ #
REMOTE_PROJECT_ROOT_PATH = '/home/binarilly/projects/binarilly.com'
REMOTE_PROJECT_DEPLOYMENT_ROOT_PATH = '/home/binarilly/deployment/projects/binarilly.com'
# ============================ REMOTE BUILDING SETTINGS ============================ #

# ============================ NGINX DEPLOYMENT SETTINGS ============================ #
NGINX_HOME = '/usr/local/nginx'
NGINX_CONF_HOME = '/usr/local/nginx/conf'
NGINX_VHOSTS_HOME = '/usr/local/nginx/conf/vhosts'
NGINX_VHOSTS_LINK_NAME = 'devtest.static.binarilly.com.conf'
NGINX_PROJECT_SETTING_FILE = 'public_static_nginx.conf'
# ============================ NGINX DEPLOYMENT SETTINGS ============================ #

# ============================ CODE SOURCE SETTINGS ============================ #
SVN_URL = 'http://svn.tools.binarilly.com:18080/svn/staticfiles/'
SVN_USERNAME = 'staticfiles'
SVN_PASSWORD = '2wsx$RFV'
# ============================ CODE SOURCE SETTINGS ============================ #
