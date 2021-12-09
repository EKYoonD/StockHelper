from django.db import models

# class Search(models.Model):
#     search_input = models.TextField()
#     result = []

#     @property
#     def findComCode(self):
#         with open('dataset/stockList.txt', encoding='utf-8') as txtfile:
#             for contents in txtfile.readlines():
#                 content =  contents.split(',')
#                 com_name = content[0]
#                 com_code = content[1]
#                 # print(com_code)
#                 if self.search_input in com_name:
#                     self.result.append(com_code)
#         return self.result
