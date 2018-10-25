from .base import BaseTag


class Concat(BaseTag):
    """
    arguments: A list of lists
    example: "`!Concat [[1, 2], [3, 4]]`"
    description: Concatenates lists.
    """
    value_types = (list,)

    def enrich(self, context):
        result = []
        for iterable in self.data:
            result.extend(context.enrich(iterable))
        return result
