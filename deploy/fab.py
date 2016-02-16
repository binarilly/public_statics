# coding=utf-8
"""
Project "publish statics" deployment toolkit.
"""
from fabric.context_managers import cd
from fabric.decorators import roles
from fabric.operations import local, put, os, run
from fabric.state import env
from deployment import DeployService, DeployByEnvService

__author__ = 'user'

env.roledefs['nginx'] = ['nginx@192.168.198.134']
env.roledefs['binarilly'] = ['binarilly@192.168.198.134']
env.roledefs['root'] = ['root@192.168.198.134']


def _switch_git_tag(git_tag):
    verify_msg = 'HEAD detached at %s' % git_tag
    status_msg = local('git status', capture=True)
    if verify_msg not in status_msg:
        checkout_msg = local('git checkout %s' % git_tag, capture=True)
        if checkout_msg.failed:
            raise Exception(checkout_msg)
    else:
        print 'GIT Code has under tag %s' % git_tag
    tag_show = local('git show %s --shortstat' % git_tag, capture=True)
    return tag_show.__str__()


def _get_svn_info(uri, reversion=None, env_string=None):
    service = DeployByEnvService(env_string)
    svn_url = service.conf.get('SVN_URL')
    url = '%s/%s' % (svn_url, uri)
    if reversion:
        url = '%s@%s' % (url, reversion)
    username = service.conf.get('SVN_USERNAME')
    password = service.conf.get('SVN_PASSWORD')
    svn_info = local('svn info %s --username %s --password %s --no-auth-cache' % (
        url, username, password
    ))
    return svn_info.__str__()


@roles('nginx')
def publish(publish_git_tag):
    """
    Publish to code to remote server.
    :return: result
    """
    # print local('git show %s' % publish_git_tag)
    git_tag_meta = _switch_git_tag(publish_git_tag)
    service = DeployService(None)
    # 清空OUTPUT
    service.clean()
    # 初始化
    service.init()
    # 打包
    tar_file_path, file_name, tar_file_name = service.build_package(publish_git_tag, git_tag_meta)
    remote_deployment_path = service.get_remote_deployment_path()
    with cd(remote_deployment_path):
        put(os.path.join(tar_file_path, tar_file_name), remote_deployment_path)
        run('tar zvxf ./%s' % tar_file_name)
        run('rm -f %s' % '%s/%s' % (service.get_remote_path(), service.get_remote_project_name()))
        run(
            'ln -s %s %s' % (
                '%s/%s' % (service.get_remote_deployment_path(), file_name), '%s/%s' % (
                    service.get_remote_path(), service.get_remote_project_name())))


def package(publish_git_tag, env_string):
    service = DeployByEnvService(env_string)
    # 清空OUTPUT
    service.clean()
    # 初始化
    service.init()
    git_tag_meta = _switch_git_tag(publish_git_tag)
    # 打包
    tar_file_path, file_name, tar_file_name = service.build_package(publish_git_tag, git_tag_meta)


def package_v2(uri, reversion, env_string):
    service = DeployByEnvService(env_string)
    # 清空OUTPUT
    service.clean()
    # 初始化
    service.init()
    svn_meta = _get_svn_info(uri, reversion, env_string)
    publish_tag = uri.replace('/', '_')
    publish_tag = '%s_%s' % (publish_tag, reversion)
    # 打包
    service.build_package(publish_tag, svn_meta)
    return publish_tag


def deploy(publish_git_tag, env_string):
    """
    Deploy package to remote
    :return:
    """
    service = DeployByEnvService(env_string)
    tar_file_name, tar_file_path = service.get_package(build_version=publish_git_tag)
    remote_deployment_root_path = service.get('REMOTE_PROJECT_DEPLOYMENT_ROOT_PATH')
    project_name = service.get('PROJECT_NAME')
    remote_deployment_path = os.path.join(remote_deployment_root_path, project_name)
    remote_deployment_path = remote_deployment_path.replace('\\', '/')
    with cd(remote_deployment_path):
        put(tar_file_path, remote_deployment_path)
        run('tar zvxf ./%s' % tar_file_name)


def relink(publish_git_tag, env_string):
    service = DeployByEnvService(env_string)
    remote_root_path = service.get('REMOTE_PROJECT_ROOT_PATH')
    project_name = service.get('PROJECT_NAME')
    remote_deployment_root_path = service.get('REMOTE_PROJECT_DEPLOYMENT_ROOT_PATH')
    remote_deployment_path = os.path.join(remote_deployment_root_path, project_name)
    remote_deployment_path = os.path.join(remote_deployment_path, '%s_%s' % (project_name, publish_git_tag))
    remote_deployment_path = remote_deployment_path.replace('\\', '/')
    with cd(remote_root_path):
        run('rm -rf %s' % project_name)
        run('ln -s %s %s' % (remote_deployment_path, project_name))

@roles('nginx')
def nginx_setting(env_string):
    service = DeployByEnvService(env_string)
    nginx_vhosts_home_path = service.conf.get('NGINX_VHOSTS_HOME')
    nginx_server_conf_name = service.conf.get('NGINX_VHOSTS_LINK_NAME')
    remote_root_path = service.conf.get('REMOTE_PROJECT_ROOT_PATH')
    project_name = service.conf.get('PROJECT_NAME')
    config_path = service.conf.get('CONFIG_OUTPUT_PATH')
    nginx_config_file = service.conf.get('NGINX_PROJECT_SETTING_FILE')
    config_path = os.path.join(remote_root_path, project_name, config_path, nginx_config_file)
    config_path = config_path.replace('\\', '/')
    with cd(nginx_vhosts_home_path):
        run('rm -rf %s' % nginx_server_conf_name)
        run('ln -s %s %s' % (config_path, nginx_server_conf_name))


@roles('root')
def nginx_reload():
    run('service nginx reload')


@roles('root')
def nginx_restart():
    run('service nginx restart')


@roles('binarilly')
def publish_v2(uri, reversion, env_string):
    publish_tag = package_v2(uri, reversion, env_string)
    deploy(publish_tag, env_string)
    relink(publish_tag, env_string)
