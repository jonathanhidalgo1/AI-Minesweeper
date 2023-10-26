import itertools

a = {("a"),("b")}
b = {("b"),("c"),("d")}

if a.isdisjoint(b) == False:
    print( b - a)

# a = {(1,0),(2,0),(2,2)}
# b = {(1,0),(1,1),(1,2)}

# new_sets = []
# for i in a:
#     for j in b:
#         if i == j:
#             print(a - b)
#         if j == i:
#             print(b - a)


# a = [{(1, 0), (1, 1)}, {(1, 0), (1, 1), (1, 2)}, {(1, 1), (1, 2)}]
# b = [{(1, 1), (1, 2)}, {(1, 0), (1, 1), (1, 2)}, {(1, 0), (1, 1)} ]

# perm = list(itertools.product(a, b))
# put_sentence_together = set()
# for cells in perm:
#     for i in cells[0]:
#         if i not in cells[1]:
#             continue
#         else:
#             put_sentence_together.add(i)
# print(put_sentence_together)
            
            
            
            
            
    # if cells[0].issubset(cells[1]):
    #     if len(cells[0]) > len(cells[1]):
    #         print(cells[0].difference(cells[1]))
    #     else:
    #         print(cells[1].difference(cells[0]))





        # a = []
        # b = []
        # # new sentence base on inference
        # for sentence in knowledge:
        #     if len(sentence.cells) == 0:
        #         continue
        #     a.append(sentence.cells)
        #     for sentence2 in reversed(knowledge):
        #         if len(sentence2.cells) == 0:
        #             continue
        #         b.append(sentence2.cells)
                
        # perm = list(itertools.product(a, b))
        # for cells in perm:
        #     if cells[0].issubset(cells[1]):
        #         if len(cells[0]) > len(cells[1]):
        #             if len(cells[0].difference(cells[1])) != 0:
        #                 print(cells[0].difference(cells[1]))
        #         else:
        #             if len(cells[1].difference(cells[0])) != 0:
        #                 print(cells[1].difference(cells[0]))
                    
