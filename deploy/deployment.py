# coding=utf-8
import logging
import os
import shutil
import datetime
import tarfile

__author__ = 'user'


formatter = logging.Formatter(
    'model:%(module)-12s fun:%(funcName)-12s line:%(lineno)-3d %(asctime)s %(levelname)-8s %(message)s',
    '%Y-%m-%d %H:%M:%S',)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__file__)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class DeployException(Exception):
    pass


class DeployIOLocalException(DeployException):
    pass


class DeploymentConfig(object):
    PROJECT_NAME = 'public_statics'

    remote_root_path = '~/deployment/www/html'
    remote_deployment_path = os.path.join(remote_root_path, 'deployments')
    remote_project_name = 'statics'

    LOCAL_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    LOCAL_OUTPUT_PATH = os.path.join(LOCAL_ROOT_PATH, 'out')
    SOURCE_PATH = os.path.join(LOCAL_ROOT_PATH, 'statics')


class DeploymentToolKit(object):
    @staticmethod
    def remove_dirs(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        logger.debug(u'Remove path: %s.' % path)

    @staticmethod
    def mkdirs(path):
        if not os.path.exists(path):
            os.makedirs(path)
        logger.debug(u'Create dirs %s.' % path)
        return path

    @staticmethod
    def copy_dirs(input_path, output_path, exclude_patterns=None):
        if not os.path.exists(input_path):
            logger.info(u'No dir is required to be copy.')
            return
        try:
            if exclude_patterns:
                shutil.copytree(input_path, output_path, ignore=shutil.ignore_patterns(*exclude_patterns))
            else:
                shutil.copytree(input_path, output_path)
        except Exception as e:
            raise e

    @staticmethod
    def copy_file(input_file, output_path):
        shutil.copyfile(input_file, output_path)

    @staticmethod
    def tar(input_path, output_path, tar_file_name=None, meta_file_name=None, meta=None, exclude=None):
        meta_file_name = '%s-deployment-meta.txt' % meta_file_name
        meta_file = os.path.join(input_path, meta_file_name)
        with open(meta_file, 'w') as tar_meta_file:
            tar_meta_file.write('Created date: %s\n' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if meta:
                tar_meta_file.write(meta)
            tar_meta_file.flush()
        name = tar_file_name
        tar_file = os.path.join(
            output_path,
            '%s.tar.gz' % name)
        tar_output = None
        try:
            tar_output = tarfile.open(tar_file, 'w|gz')
            print 'tar input path %s' % input_path
            tar_output.add(name=input_path, arcname=name, exclude=exclude)
        finally:
            if tar_output:
                tar_output.close()

        # with tarfile.open(tar_file, 'w|gz') as tar_output:
        #     tar_output.add(name=input_path, arcname=name, exclude=None)


class DeployService(object):
    """
    发布服务
    """
    _conf = {
        'PROJECT_NAME': DeploymentConfig.PROJECT_NAME,
        'LOCAL_OUTPUT_PATH': DeploymentConfig.LOCAL_OUTPUT_PATH,
        'SOURCE_PATH': DeploymentConfig.SOURCE_PATH,
    }

    def __init__(self, conf):
        super(DeployService, self).__init__()
        if not conf:
            self.conf = self._conf
        else:
            self.conf = conf

    def clean(self):
        local_output_path = self.conf.get('LOCAL_OUTPUT_PATH', None)
        if not local_output_path:
            raise DeployIOLocalException(u'Execute clean unsuccessfully, cause of output folder is not set.')
        if os.path.exists(local_output_path):
            DeploymentToolKit.remove_dirs(local_output_path)
        logger.info('Deployment local output folder cleared.')

    def init(self):
        local_output_path = self.conf.get('LOCAL_OUTPUT_PATH', None)
        DeploymentToolKit.mkdirs(local_output_path)

    def build_package(self):
        local_output_path = self.conf.get('LOCAL_OUTPUT_PATH', None)
        source_path = self.conf.get('SOURCE_PATH', None)
        if not source_path:
            raise DeployIOLocalException(u'No source code can be found.')
        to_deployment_path = os.path.join(local_output_path, self.conf.get('PROJECT_NAME'))
        DeploymentToolKit.copy_dirs(source_path, to_deployment_path)
        logger.info('Copy source file %s to output path %s.' % (source_path, to_deployment_path))
