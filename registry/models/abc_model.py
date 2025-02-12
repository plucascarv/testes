from abc import ABCMeta, abstractmethod
from django.db import models


class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class ABCModel(models.Model, metaclass=AbstractModelMeta):

    @abstractmethod
    def validate_doc(self):
        raise NotImplementedError(
            "Please implement document validation in concrete class"
        )

    class Meta:
        abstract = True
