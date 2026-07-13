from copy import deepcopy, copy


class HistoryDict:
    def __init__(self, data: dict = None):
        if data is None:
            self._data = {}
        else:
            self._data = {key: [value] for key, value in data.items()}


    def keys(self):
        yield from self._data.keys()

    def values(self):
        yield from (value[-1] for value in self._data.values())

    def items(self):
        yield from ((key, value[-1])for key,value in self._data.items())

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        yield from self._data

    def __getitem__(self, key):
        return self._data[key][-1]

    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key].append(value)
        else:
            self._data[key] = [value]

    def __delitem__(self,key):
        del self._data[key]

    def history(self, key):
        return self._data.get(key, [])

    def all_history(self):
        return deepcopy(self._data)


class Grouper:
    def __init__(self, iterable, key):
        self._key = key
        self._groups = {}
        for item in iterable:
            self.add(item)

    def add(self, item):
        group_key = self._key(item)
        if group_key not in self._groups:
            self._groups[group_key] = [item]
        else:
            self._groups[group_key].append(item)

    def group_for(self, item):
        return self._key(item)

    def __len__(self):
        return len(self._groups)

    def __iter__(self):
        yield from self._groups.items()

    def __contains__(self, item):
        return item in self._groups

    def __getitem__(self, key):
        return self._groups[key]

# class SequenceZip:
#     def __init__(self, *args):
#         self._items = tuple(tuple(arg) for arg in args)
#
#     def __len__(self):
#         if not self._items:
#             return 0
#         return min(len(seq) for seq in self._items)
#
#     def __iter__(self):
#         yield from zip(*self._items)
#
#     def __getitem__(self,key):
#         return (seq[key] for seq in self._items)

import copy

class SequenceZip:
    def __init__(self, *iterables):
        self.iterables = copy.deepcopy(iterables)

    def __len__(self):
        return min((len(s) for s in self.iterables), default=0)

    def __getitem__(self, index):
        return tuple(s[index] for s in self.iterables)

    def __iter__(self):
        yield from zip(*self.iterables)



class MutableString:
    def __init__(self, string: str = None):
        if string is None:
            self._string = []
        else:
            self._string = list(string)

    def lower(self):
        self._string = [char.lower() for char in self._string]

    def upper(self):
        self._string = [char.upper() for char in self._string]

    def __str__(self):
        return ''.join(self._string)

    def __repr__(self):
        return f"MutableString('{''.join(self._string)}')"

    def __len__(self):
        return len(self._string)

    def __iter__(self):
        yield from self._string

    def __getitem__(self, key):
        if isinstance(key, slice):
            return MutableString(''.join(self._string[key]))
        return MutableString(self._string[key])

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self._string[key] = list(value)
        else:
            if key < 0:
                key = len(self._string) + key
            self._string[key:key + 1] = list(value)

    def __delitem__(self, key):
        del self._string[key]

    def __add__(self, other):
        if isinstance(other, MutableString):
            return MutableString(str(self) + str(other))
        elif isinstance(other, str):
            return MutableString(str(self) + other)
        return NotImplemented

# TEST_13:
mutablestring = MutableString('beegeek')

mutablestring[-1] = 'ee'
print(mutablestring)

mutablestring[-2:] = 'geek'
print(mutablestring)


class NonEmptyString:
    def __init__(self, attr):
        self._attr = attr

    def __get__(self, obj, cls):
        if self._attr in obj.__dict__:
            return obj.__dict__[self._attr]
        else:
            raise AttributeError('Атрибута не существует')

    def __set__(self, obj, value):
        if isinstance(value, str) and len(value) > 0:
            obj.__dict__[self._attr] = value
        else:
            raise ValueError('Некорректное значение')

    def __delete__(self, obj):
        del obj.__dict__[self._attr]


class Cat:
    name = NonEmptyString('name')

    def __init__(self, name):
        self.name = name


cat = Cat('Кемаль')
print(cat.name)

cat.name = 'Роджер'
print(cat.name)

del cat.name
print(hasattr(cat, 'name'))
