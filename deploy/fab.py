# coding=utf-8
"""
Project "publish statics" deployment toolkit.
"""
from fabric.operations import local
from deployment import DeployService

__author__ = 'user'


def publish(publish_git_tag):
    """
    Publish to code to remote server.
    :return: result
    """
    service = DeployService(None)
    # 清空OUTPUT
    service.clean()
    # 初始化
    service.init()
    # 打包
    service.build_package()
