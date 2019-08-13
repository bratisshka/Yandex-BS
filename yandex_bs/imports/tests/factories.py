import factory

from yandex_bs.imports.models import ImportObject, Citizen


class ImportFactory(factory.DjangoModelFactory):
    class Meta:
        model = ImportObject


class CitizenFactory(factory.DjangoModelFactory):
    class Meta:
        model = Citizen

    import_object = factory.SubFactory(ImportFactory)
