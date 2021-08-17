from munch import *
from munch import Munch as OldMunch


class Munch(OldMunch):
    def __init__(self, *args, **kwargs):
        super(Munch, self).__init__(*args, **kwargs)
        self.update(munchify(self))
    
    def to_dict(self):
        """
        Recursively converts a NCObject back into a dictionary.
        >>> b = NCObject(foo=NCObject(lol=True), hello=42, ponies='are pretty!')
        >>> sorted(b.to_dict().items())
        [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]
        """
        return self.toDict()

    def to_json(self):
        return self.toJSON()