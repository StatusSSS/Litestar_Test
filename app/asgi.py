from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from advanced_alchemy.extensions.litestar.plugins import (
    SQLAlchemyInitPlugin,
    SQLAlchemySerializationPlugin,
)
from advanced_alchemy.extensions.litestar.plugins.init.config import (
    SQLAlchemyAsyncConfig,
)

from .routes import UserController
from .settings import get_settings



settings = get_settings()

sqlalchemy_plugin = SQLAlchemyInitPlugin(
    SQLAlchemyAsyncConfig(
        connection_string=settings.database_url,
        session_dependency_key="session",
    )
)

app = Litestar(
    route_handlers=[UserController],
    plugins=[sqlalchemy_plugin, SQLAlchemySerializationPlugin()],
    openapi_config=OpenAPIConfig(
        title="User Management API",
        version="1.0.0",
        description="CRUD для таблицы user",
        render_plugins=[SwaggerRenderPlugin(path="/docs")],
    ),
    debug=settings.debug,
)