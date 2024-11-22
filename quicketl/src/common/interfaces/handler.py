# from abc import ABC, abstractmethod
# from typing import List

# from quicketl.src.common.dtos.contracts.contract import Contract
# from quicketl.src.common.dtos.time_travel.predicate import Predicate


# class ContractHandler(ABC):

#     @abstractmethod
#     def capture_contract(self) -> None:
#         raise NotImplementedError

#     @abstractmethod
#     def get_contract(self) -> Contract:
#         pass


# class TimeTravelHandler(ContractHandler):

#     @abstractmethod
#     def get_date_predicate(self) -> Predicate:
#         pass

#     @abstractmethod
#     def get_categoric_predicate(self) -> List[Predicate]:
#         pass

#     @abstractmethod
#     def get_categoric_predicates(self) -> List[Predicate]:
#         pass

#     @abstractmethod
#     def get_optimal_predicates(self) -> List[Predicate]:
#         pass

#     @abstractmethod
#     def get_processed_predicates(self) -> List[Predicate]:
#         pass

#     @abstractmethod
#     def get_push_down(self) -> str:
#         pass


# class ProcessHandler(ContractHandler):
#     pass
