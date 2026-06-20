class Todo:
    def __init__(self):
        self.things = []

    def add(self, name, priority):
        self.things.append((name, priority))

    def get_by_priority(self, priority):
        return [key for key, value in self.things if value == priority]

    def get_low_priority(self):
        if not self.things:  # проверка на пустой список
            return []
        low_priority = min(self.things, key=lambda x: x[1])[1]
        return [key for key, value in self.things if value == low_priority]

    def get_high_priority(self):
        if not self.things:  # проверка на пустой список
            return []
        high_priority = max(self.things, key=lambda x: x[1])[1]
        return [key for key, value in self.things if value == high_priority]

    class Todo:
        def __init__(self):
            self.things = []

        def add(self, name, priority):
            self.things.append((name, priority))

        def get_by_priority(self, priority):
            return [name for name, pr in self.things if pr == priority]

        def get_low_priority(self):
            if not self.things:
                return []
            return self.get_by_priority(min(self.things, key=lambda x: x[1])[1])

        def get_high_priority(self):
            if not self.things:
                return []
            return self.get_by_priority(max(self.things, key=lambda x: x[1])[1])

# class Todo:
#     def __init__(self):
#         self.things = []
#
#     def add(self, name, priority):
#         self.things.append((name, priority))
#
#     def get_by_priority(self, priority):
#         return [name for name, pr in self.things if pr == priority]
#
#     def get_low_priority(self):
#         if not self.things:
#             return []
#         return self.get_by_priority(min(self.things, key=lambda x: x[1])[1])
#
#     def get_high_priority(self):
#         if not self.things:
#             return []
#         return self.get_by_priority(max(self.things, key=lambda x: x[1])[1])