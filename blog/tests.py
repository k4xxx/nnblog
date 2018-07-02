from django.test import TestCase

# Create your tests here.

# s = '<div><h1>good</h1></div>'.replace(r'/<[^>]+>/g',"")
# print(s)

# import re
# html='<div><h1>good</h1></div>'
# dr = re.compile(r'<[^>]+>',re.S).sub('',html)
# # dd = dr.sub('',html)
# print(dr)
# d={
#     1: {
#         "urls": ['/users/', '/users/add/', '/users/delete/(\\d+)', 'users/edit/(\\d+)'],
#         "actions": ['list', "add", 'delete', 'edit']
#     },
#     2: {
#         "urls": ['/roles/'],
#         "actions": ['list']
#     }
# }
# l = [{'permissions__url': '/users/',
#   'permissions__group_id': 1,
#   'permissions__action': 'list'},
#  {'permissions__url': '/users/add/',
#   'permissions__group_id': 1,
#   'permissions__action': 'add'},
#  {'permissions__url': '/users/delete/(\\d+)',
#   'permissions__group_id': 1,
#   'permissions__action': 'delete'},
#  {'permissions__url': 'users/edit/(\\d+)',
#   'permissions__group_id': 1,
#   'permissions__action': 'edit'},
#  {'permissions__url': '/roles/',
#   'permissions__group_id': 2,
#   'permissions__action': 'list'}
#  ]
# l =[]
# for x,y in d.items():
#     for i in range(len(y['urls'])):
#         l.append({'permissions__url':y['urls'][i],'permissions__group_id':x,'permissions__action':y['actions'][i]})
#
# print(l)