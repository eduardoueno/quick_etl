from quicketl.src.common.utils import get_src_path


print(get_src_path())

# from quicketl.src.common.dtos.time_travel.predicate import Predicate
# from quicketl.src.common.dtos.time_travel.condition import Condition
# from quicketl.src.common.factories.get_condition import get_condition
# from quicketl.src.common.utils import remove_dups

# import typing

# typing.TYPE_CHECKING = True

# pre_1 = Predicate(**{"column_name": "pre1", "operator": "=", "value": "0"})
# pre_2 = Predicate(**{"column_name": "pre1", "operator": "=", "value": "0"})

# print(pre_1)
# print(pre_2)

# if pre_1 == pre_2:
#     print("Eita")

# cond_1 = Condition(
#     **{
#         "predicates": [
#             {"column_name": "pre1", "operator": "=", "value": "0"},
#             {"column_name": "pre1", "operator": "=", "value": "0"},
#         ]
#     }
# )
# cond_2 = Condition(
#     **{
#         "predicates": [
#             pre_1,
#             pre_2,
#         ]
#     }
# )

# print(cond_1)
# print(cond_2)

# if cond_1 == cond_2:
#     print("Eita2")

# print("dups")
# dups = [cond_1, cond_2]
# print(dups)
# print(remove_dups(dups))
# print(dups)

# print("TCHECK")
# cond_3 = get_condition(
#     predicates=[
#         {"column_name": "pre1", "operator": "=", "value": "0"},
#         {"column_name": "pre1", "operator": "=", "value": "0"},
#         pre_1,
#         # "str",
#     ]
# )

# print(cond_3)
