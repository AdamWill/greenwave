# SPDX-License-Identifier: GPL-2.0+
import os


def _local_conf_dir(subdir):
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(basedir, 'conf', subdir)


class Config(object):
    """
    A GreenWave Flask configuration.
    """
    DEBUG = True
    # We configure logging explicitly, turn off the Flask-supplied log handler.
    LOGGER_HANDLER_POLICY = 'never'
    HOST = '127.0.0.1'
    PORT = 5005
    PRODUCTION = False
    SECRET_KEY = 'replace-me-with-something-random'  # nosec

    RESULTSDB_API_URL = 'https://taskotron.fedoraproject.org/resultsdb_api/api/v2.0'
    WAIVERDB_API_URL = 'https://waiverdb.fedoraproject.org/api/v1.0'

    # Remote rule configuration
    # NOTE: DIST_GIT_URL_TEMPLATE is obsolete and used here only for
    # backward compatibility. They maybe removed in future versions. Use REMOTE_RULE_POLICIES['*']
    # instead
    DIST_GIT_URL_TEMPLATE = \
        'https://src.fedoraproject.org/{pkg_namespace}{pkg_name}/raw/{rev}/f/gating.yaml'
    REMOTE_RULE_POLICIES = {
        'brew-build-group': (
            'https://git.example.com/devops/greenwave-policies/side-tags/raw/master/'
            '{subject_id}.yaml'
        ),
        '*': 'https://src.fedoraproject.org/{pkg_namespace}{pkg_name}/raw/{rev}/f/gating.yaml'
    }
    REMOTE_RULE_GIT_TIMEOUT = 30
    REMOTE_RULE_GIT_MAX_RETRY = 3
    KOJI_BASE_URL = 'https://koji.fedoraproject.org/kojihub'
    # Options for outbound HTTP requests made by python-requests
    REQUESTS_TIMEOUT = (6.1, 15)
    REQUESTS_VERIFY = True

    POLICIES_DIR = '/etc/greenwave/policies'
    SUBJECT_TYPES_DIR = '/etc/greenwave/subject_types'

    MESSAGING = 'fedmsg'

    # By default, don't cache anything.
    CACHE = {'backend': 'dogpile.cache.null'}
    # Greenwave API url
    GREENWAVE_API_URL = 'https://greenwave.domain.local/api/v1.0'

    OUTCOMES_PASSED = ('PASSED', 'INFO')
    OUTCOMES_ERROR = ('ERROR',)
    OUTCOMES_INCOMPLETE = ('QUEUED', 'RUNNING')


class ProductionConfig(Config):
    DEBUG = False
    PRODUCTION = True


class DevelopmentConfig(Config):
    #RESULTSDB_API_URL = 'https://taskotron.stg.fedoraproject.org/resultsdb_api/api/v2.0'
    RESULTSDB_API_URL = 'http://localhost:5001/api/v2.0'
    #WAIVERDB_API_URL = 'http://waiverdb-dev.fedorainfracloud.org/api/v1.0'
    WAIVERDB_API_URL = 'http://localhost:5004/api/v1.0'
    GREENWAVE_API_URL = 'http://localhost:5005/api/v1.0'
    POLICIES_DIR = _local_conf_dir('policies')
    SUBJECT_TYPES_DIR = _local_conf_dir('subject_types')
    REMOTE_RULE_POLICIES = {
        'brew-build-group': (
            'https://git.example.com/devops/greenwave-policies/side-tags/raw/master/{pkg_namespace}'
            '{pkg_name}.yaml'
        ),
        '*': 'https://src.fedoraproject.org/{pkg_namespace}{pkg_name}/raw/{rev}/f/gating.yaml'
    }


class TestingConfig(Config):
    RESULTSDB_API_URL = 'http://localhost:5001/api/v2.0'
    WAIVERDB_API_URL = 'http://localhost:5004/api/v1.0'
    GREENWAVE_API_URL = 'http://localhost:5005/api/v1.0'
    KOJI_BASE_URL = 'http://localhost:5006/kojihub'
    POLICIES_DIR = _local_conf_dir('policies')
    SUBJECT_TYPES_DIR = _local_conf_dir('subject_types')


class FedoraTestingConfig(Config):
    RESULTSDB_API_URL = 'http://localhost:5001/api/v2.0'
    WAIVERDB_API_URL = 'http://localhost:5004/api/v1.0'
    GREENWAVE_API_URL = 'http://localhost:5005/api/v1.0'
    KOJI_BASE_URL = 'http://localhost:5006/kojihub'
    POLICIES_DIR = _local_conf_dir('policies')
