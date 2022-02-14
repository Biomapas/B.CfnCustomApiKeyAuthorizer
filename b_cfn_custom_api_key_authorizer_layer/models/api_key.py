import logging

from b_lambda_layer_common.exceptions.container.internal_error import InternalError
from b_lambda_layer_common.exceptions.container.not_found_error import NotFoundError
from b_lambda_layer_common.util.os_parameter import OSParameter
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist, GetError
from pynamodb.models import Model

API_KEYS_DATABASE_NAME = OSParameter('API_KEYS_DATABASE_NAME')
API_KEYS_DATABASE_REGION = OSParameter('API_KEYS_DATABASE_REGION')

logger = logging.getLogger(__name__)


class ApiKey(Model):
    """
    DynamoDB group model representation.
    """

    class Meta:
        table_name = API_KEYS_DATABASE_NAME.value
        region = API_KEYS_DATABASE_REGION.value

    # Unique group identifier.
    __pk = UnicodeAttribute(attr_name='pk', hash_key=True)

    @property
    def key(self) -> str:
        return self.__pk

    @key.setter
    def key(self, value: str) -> None:
        self.__pk = value

    """
    Methods.
    """

    @classmethod
    def get_api_key(cls, key: str) -> 'ApiKey':
        """
        Gets api key entity from DynamoDB table.

        :return: Api key entity.
        """
        try:
            # noinspection PyTypeChecker
            return cls.get(hash_key=key)
        except DoesNotExist:
            raise NotFoundError('Api key not found.')
        except GetError as ex:
            logger.exception('Failed to get Api key.')
            raise InternalError(f'Could not get Api key. Reason: {repr(ex)}.')