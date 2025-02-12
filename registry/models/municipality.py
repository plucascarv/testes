from django.db import models


class Municipality(models.Model):
    city_name = models.CharField(max_length=100)
    city_id = models.IntegerField()
    state = models.CharField(max_length=100)
    ibge_id = models.IntegerField()

    def __str__(self):
        return self.city_name

    def get_city_id(self):
        return self.city_id

    def get_state(self):
        return self.state

    def get_name(self):
        return self.city_name

    def set_ibge_id(self, ibge_id: int):
        self.ibge_id = ibge_id

    def validate_ibge_id(self, ibge_id: int) -> bool:
        return isinstance(ibge_id, int) and 1000000 <= ibge_id <= 9999999

    class Meta:
        abstract = True
        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"
