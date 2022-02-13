# Import all the fixtures.
# noinspection PyUnresolvedReferences
from b_cfn_custom_api_key_authorizer_test.integration.manager import MANAGER

from b_cfn_custom_api_key_authorizer_test.integration.fixtures import *

from b_cfn_custom_api_key_authorizer_test.integration.infra_create import inf_create
from b_cfn_custom_api_key_authorizer_test.integration.infra_destroy import inf_destroy


def pytest_sessionstart(session):
    MANAGER.set_global_prefix('LaimonasAuthorizer')
    inf_create()


def pytest_sessionfinish(session, exitstatus):
    MANAGER.set_global_prefix('LaimonasAuthorizer')
    # inf_destroy()
