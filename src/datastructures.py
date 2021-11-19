
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        self._members = [
            {"id":1, "first_name":"John Jackson", "age":33, "lucky numbers": [7, 13, 22]},
            {"id":2, "first_name":"Jane Jackson", "age":35, "lucky_numbers": [10, 14, 3]},
            {"id":3, "first_name":"Jimmy Jackson", "age":5, "lucky_numbers": [1]}
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        r = randint(1, 99999999)
        if self.get_member(r):
            r = self._generateId()
        return r

    def add_member(self, member):
        value = {
            "id" : self._generateId() if member.get('id') is None else member.get('id'),
            "first_name" : member.get('first_name'),
            "last_name" : self.last_name,
            "age" : member.get('age'),
            "lucky_numbers" : member.get('lucky_numbers')
        }
        self._members.append(value)
        return value

    def update_member(self, id, member):
        ## labels not presents in member remain with his olds values
        index = 0
        while (index<len(self._members)) and (self._members[index].get('id') != id): index += 1
        if index == len(self._members):
            return None
        else:
            old_values = self._members[index]
            value = {
                'id' : id,
                'first_name' : member.get('first_name') if member.get('first_name') else old_values.get('first_name'),
                'last_name' : self.last_name,
                'age' : member.get('age') if member.get('age') else old_values.get('age'),
                'lucky_numbers' : member.get('lucky_numbers') if member.get('lucky_numbers') else old_values.get('lucky_numbers')
            }
            self._members[index] = value
            return value

    def delete_member(self, id):
        # fill this method and update the return
        index = 0
        while (index<len(self._members)) and (self._members[index].get('id') != id): index += 1
        if index == len(self._members):
            return None
        else:
            del self._members[index]
            return index

    def get_member(self, id):
        # fill this method and update the return
        index = 0
        while index<len(self._members) and self._members[index].get('id') != id: index += 1 # buscamos el índice
        if index == len(self._members):
            return None
        else:
            return self._members[index]

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        list = self._members
        return list