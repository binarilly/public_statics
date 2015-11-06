# coding=utf-8
"""
发布静态公共资源
"""
import os

__author__ = 'user'


class DeploymentConfig(object):
    remote_root_path = '~/deployment/www/html'
    remote_deployment_path = os.path.join(remote_root_path, 'deployments')
    remote_project_name = 'statics'
