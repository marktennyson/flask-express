from munch import *
from json import dumps
from munch import Munch as OldMunch


class Munch(OldMunch):
    def __init__(self, *args, **kwargs):
        super(Munch, self).__init__(*args, **kwargs)
        self.update(munchify(self))
    
    def to_dict(self):
        """
        Recursively converts a Munch back into a dictionary.
        >>> b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
        >>> sorted(b.to_dict().items())
        [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]
        """
        return self.toDict()

    def to_json(self):
        """
        Recursively converts a Munch back into a dictionary.
        And provide the json encoded string data.
        """
        return dumps(self.toDict())