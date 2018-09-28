from collections.abc import Mapping, Sequence

from .base import BaseTag


def get_iterable(tag, over, context, index_start=None):
    if isinstance(over, str) and over in context:
        # This does mean you can't explicitly iterate over strings that are keys
        # in the context, but if you really do need to do that, you may need to
        # rethink your approach anyway.
        raise ValueError(
            f'{tag}: `over` value exists within the context; did you mean `!Var {over}`?'
        )

    if hasattr(over, 'enrich'):
        over = over.enrich(context)

    if isinstance(over, Mapping):
        if index_start is not None:
            raise ValueError('cannot use index_start with dict')

        return (over.items(), True)

    if isinstance(over, Sequence):
        if index_start is None:
            index_start = 0

        return (enumerate(over, index_start), False)

    raise ValueError(f'{tag}: over value {over} is not iterable')


class Loop(BaseTag):
    value_types = (dict,)

    def enrich(self, context):
        from ..context import Context

        as_ = str(self.data.get('as', 'item'))
        index_as = str(self.data.get('index_as') or '')
        compact = bool(self.data.get('compact'))
        index_start = self.data.get('index_start')

        template = self.data.get('template')
        if template is None:
            raise ValueError(f'{self}: missing template')

        output = []
        iterable, _ = self.get_iterable(context, index_start)
        for index, value in iterable:
            subcontext = {as_: value}
            if index_as:
                subcontext[index_as] = index
            value = Context(context, subcontext).enrich(template)
            if compact and not value:
                continue
            output.append(value)
        return output

    def get_iterable(self, context, index_start):
        return get_iterable(self, self.data.get('over'), context, index_start)
