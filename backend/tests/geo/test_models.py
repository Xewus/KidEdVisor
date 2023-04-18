import pytest
from src.core.enums import TableNames
from src.db.postgres import Base
from src.geo import (
    AddressModel,
    AddressScheme,
    CityModel,
    CountryModel,
    DistrictModel,
    RegionModel,
    StreetModel,
    address_crud,
)
from tests.conftest import get_test_db
from tests.geo.conftest import (
    AddressAttrs,
    TestAddresses,
    TestCities,
    TestCountries,
    TestDistricts,
    TestRegions,
    TestStreets,
)


@pytest.mark.models
@pytest.mark.parametrize(
    "Model, table_name, fields",
    [
        # 0 CountryModel
        (
            CountryModel,
            TableNames.COUNTRY,
            {"id", "name"},
        ),
        # 1 RegionModel
        (
            RegionModel,
            TableNames.REGION,
            {"id", "name", "country_id"},
        ),
        # 2 DistrictModel
        (
            DistrictModel,
            TableNames.DISTRICT,
            {"id", "name", "region_id"},
        ),
        # 3 CityModel
        (
            CityModel,
            TableNames.CITY,
            {"id", "name", "country_id", "region_id", "district_id"},
        ),
        # 4 StreetModel
        (
            StreetModel,
            TableNames.STREET,
            {"id", "name", "city_id"},
        ),
        # 5 AddressModel
        (
            AddressModel,
            TableNames.ADDRESS,
            {"id", "city_id", "street_id", "building", "adds", "office"},
        ),
    ],
)
def test_geo_models_attrs(Model: Base, table_name: str, fields: set[str]):
    assert Model.__tablename__ == table_name, (
        "Unexpected table name for `%s`" % Model
    )
    assert set(col.name for col in Model.__table__.columns) == fields, (
        "Unexpected fields in the `%s`" % Model
    )


@pytest.mark.crud
@pytest.mark.parametrize(
    "address, expect",
    [
        # 0 country + not exist city
        (
            AddressScheme(
                country=TestCountries.country_2.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_2,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 1 country + region + not exist city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                None,
                None,
                None,
                None,
            ),
        ),
        # 2 country + invalid region + not exist city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 3 country + region + district + not exist city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                district=TestDistricts.district_1_1_1.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                TestDistricts.district_1_1_1,
                None,
                None,
                None,
            ),
        ),
        # 4 country + invalid region + district + not exist city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                district=TestDistricts.district_2_3_3.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 5 country + region + invalid  district + not exist city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                district=TestDistricts.district_2_3_3.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                None,
                None,
                None,
                None,
            ),
        ),
        # 6 country + invalid region + invalid  district + not exist city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                district=TestDistricts.district_3_4_4.name,
                city="Not exists",
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 7 country + city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                city=TestCities.city_1_0_0_1.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                TestCities.city_1_0_0_1,
                None,
                None,
            ),
        ),
        # 8 country + region + city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                city=TestCities.city_1_1_0_2.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                None,
                TestCities.city_1_1_0_2,
                None,
                None,
            ),
        ),
        # 9 country + region + district + city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                district=TestDistricts.district_1_1_1.name,
                city=TestCities.city_1_1_1_3.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                TestDistricts.district_1_1_1,
                TestCities.city_1_1_1_3,
                None,
                None,
            ),
        ),
        # 10 country + invalid region + city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                city=TestCities.city_1_0_0_1.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 11 country + invalid region + invalid city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                city=TestCities.city_2_0_0_4.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 12 country + invalid region + district + city
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                district=TestDistricts.district_1_1_1.name,
                city=TestCities.city_1_1_1_3.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 13 country + city + street
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                city=TestCities.city_1_0_0_1.name,
                street=TestStreets.street_1_0_0_1_1.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                TestCities.city_1_0_0_1,
                TestStreets.street_1_0_0_1_1,
                None,
            ),
        ),
        # 14 country + region + district + city + street
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                district=TestDistricts.district_1_1_1.name,
                city=TestCities.city_1_1_1_3.name,
                street=TestStreets.street_1_1_1_3_3.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                TestDistricts.district_1_1_1,
                TestCities.city_1_1_1_3,
                TestStreets.street_1_1_1_3_3,
                None,
            ),
        ),
        # 15 country + invalid region + district + city + street
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_2_3.name,
                district=TestDistricts.district_1_1_1.name,
                city=TestCities.city_1_1_1_3.name,
                street=TestStreets.street_1_1_1_3_3.name,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                None,
                None,
                None,
            ),
        ),
        # 16 country + city + address with building
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                city=TestCities.city_1_0_0_1.name,
                building=TestAddresses.address_1_0_0_1_0_1.building,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                TestCities.city_1_0_0_1,
                None,
                TestAddresses.address_1_0_0_1_0_1,
            ),
        ),
        # 17 country + city + address with adds
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                city=TestCities.city_1_0_0_1.name,
                adds=TestAddresses.address_1_0_0_1_0_2.adds,
            ),
            AddressAttrs(
                TestCountries.country_1,
                None,
                None,
                TestCities.city_1_0_0_1,
                None,
                TestAddresses.address_1_0_0_1_0_2,
            ),
        ),
        # 18 country + + region + district + city + street +
        # address with adds, building, office
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                district=TestDistricts.district_1_1_1.name,
                city=TestCities.city_1_1_1_3.name,
                street=TestStreets.street_1_1_1_3_3.name,
                adds=TestAddresses.address_1_1_1_3_1_3.adds,
                building=TestAddresses.address_1_1_1_3_1_3.building,
                office=TestAddresses.address_1_1_1_3_1_3.office,
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                TestDistricts.district_1_1_1,
                TestCities.city_1_1_1_3,
                TestStreets.street_1_1_1_3_3,
                TestAddresses.address_1_1_1_3_1_3,
            ),
        ),
        # 19 country + + region + district + city + street +
        # address with adds, building,  invalid office
        (
            AddressScheme(
                country=TestCountries.country_1.name,
                region=TestRegions.region_1_1.name,
                district=TestDistricts.district_1_1_1.name,
                city=TestCities.city_1_1_1_3.name,
                street=TestStreets.street_1_1_1_3_3.name,
                adds=TestAddresses.address_1_1_1_3_1_3.adds,
                building=TestAddresses.address_1_1_1_3_1_3.building,
                office="invalid",
            ),
            AddressAttrs(
                TestCountries.country_1,
                TestRegions.region_1_1,
                TestDistricts.district_1_1_1,
                TestCities.city_1_1_1_3,
                TestStreets.street_1_1_1_3_3,
                None,
            ),
        ),
    ],
)
async def test_get_full_address(
    set_addresses, address: AddressScheme, expect: AddressAttrs
):
    db = await anext(get_test_db())

    try:
        full_address = await address_crud.get_full_address(db, address)
        assert full_address.country.name == expect.country.name

        if expect.region is None:
            assert full_address.region is None
        else:
            assert full_address.region.name == expect.region.name

        if expect.district is None:
            assert full_address.district is None
        else:
            assert full_address.district.name == expect.district.name

        if expect.city is None:
            assert full_address.city is None
        else:
            assert full_address.city.name == expect.city.name

        if expect.street is None:
            assert full_address.street is None
        else:
            assert full_address.street.name == expect.street.name

        if expect.address is None:
            assert full_address.address is None
        else:
            assert full_address.address.building == expect.address.building
            assert full_address.address.adds == expect.address.adds
            assert full_address.address.office == expect.address.office

    finally:
        await db.close()
