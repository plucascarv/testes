from abc import ABC, ABCMeta, abstractmethod
from django.db.models.base import ModelBase


class ValidateDocument(ABC):
    @abstractmethod
    def validate_doc(self):
        raise NotImplementedError(
            "Please implement document validation in concrete class"
        )


class ModelABCMeta(ModelBase, ABCMeta):
    pass
