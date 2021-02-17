from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

import logging
logger = logging.getLogger(__name__)


class SharedAPIRootRouter(SimpleRouter):
    shared_router = DefaultRouter()

    def register(self, *args, **kwargs):
        logger.info(f'registering new views: args: {args}, kwargs: {kwargs}')
        self.shared_router.register(*args, **kwargs)
        super().register(*args, **kwargs)


def collect_api_urls():
    """
    Import the urls.py module from each INSTALLED_APP so that each app can register
    it's REST API ViewSets with the single SharedAPIRootRouter().

    Conventions assumed:
    1. your app is added to the Installed

    In the `<your_app>/urls.py` it should look like this:

    ```python
    from tom_common.api_router import SharedAPIRootRouter
    router = SharedAPIRootRouter()
    router.register(r'your_app', YourAppModelViewSet)
    ```
    :return: list of router.urls collected from all INSTALLED_APPS with urls.py modules
    """
    from importlib import import_module
    for app in settings.INSTALLED_APPS:
        logger.debug(f'looking in {app} for urls.py')
        try:
            import_module(app + '.urls')  # by convention where the REST API routes are defined.
        except (ImportError, AttributeError) as err:
            logger.debug(f'Failed to import urls from {app} err: {err}')
    return SharedAPIRootRouter.shared_router.urls