import factory

from yandex_bs.imports.models import ImportObject, Citizen


class ImportFactory(factory.DjangoModelFactory):
    class Meta:
        model = ImportObject


class CitizenFactory(factory.DjangoModelFactory):
    class Meta:
        model = Citizen

    import_object = factory.SubFactory(ImportFactory)
    citizen_id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    town = factory.Faker("city")
    street = factory.Faker("street_name")
    building = factory.Faker("secondary_address")
    apartment = factory.Faker("random_int", min=1)
    birth_date = factory.Faker("date_of_birth")
    gender = factory.Faker("random_element", elements=(Citizen.MALE, Citizen.FEMALE))

    def relatives(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, list):
                self.relatives = extracted
