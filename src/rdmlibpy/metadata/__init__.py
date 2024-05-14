# set package version
__version__ = '0.1.1'

from .metadata import Metadata, MetadataDict, MetadataList, MetadataNode
from .queries import query
from .resolvers import register_custom_resolvers

# register custom resolvers
register_custom_resolvers()

__all__ = [
    Metadata,
    MetadataNode,
    query,
    register_custom_resolvers,
]  # type: ignore
