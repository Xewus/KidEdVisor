from collections import namedtuple
from typing import Any, Generator

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.enums import Countries, TableNames
from src.geo import (
    AddressModel,
    CityModel,
    CountryModel,
    DistrictModel,
    RegionModel,
    StreetModel,
)
from tests.conftest import get_test_db

AddressAttrs = namedtuple(
    "AddressAttrs", "country region district city street address"
)


class Values:
    @classmethod
    def values(cls) -> Generator[Any, None, None]:
        return (v for k, v in cls.__dict__.items() if not k.startswith("_"))

    @classmethod
    async def to_db(cls, db: AsyncSession):
        db.add_all(cls.values())
        await db.flush()


class TestCountries(Values):
    country_1 = CountryModel(name=Countries.AFGHANISTAN)
    country_2 = CountryModel(name=Countries.BENIN)
    country_3 = CountryModel(name=Countries.CHAD)


class TestRegions(Values):
    region_1_1 = RegionModel(name="TestRegion_1_1", country_id=1)
    region_1_2 = RegionModel(name="TestRegion_1_2", country_id=1)
    region_2_3 = RegionModel(name="TestRegion_2_3", country_id=2)
    region_3_4 = RegionModel(name="TestRegion_3_4", country_id=3)


class TestDistricts(Values):
    district_1_1_1 = DistrictModel(name="TestDistrict_1_1_1", region_id=1)
    district_1_1_2 = DistrictModel(name="TestDistrict_1_1_2", region_id=1)
    district_2_3_3 = DistrictModel(name="TestDistrict_2_3_3", region_id=2)
    district_3_4_4 = DistrictModel(name="TestDistrict_3_4_4", region_id=4)


class TestCities(Values):
    city_1_0_0_1 = CityModel(name="TestCity_1_0_0_1", country_id=1)
    city_1_1_0_2 = CityModel(
        name="TestCity_1_1_0_2", country_id=1, region_id=1
    )
    city_1_1_1_3 = CityModel(
        name="TestCity_1_1_1_3", country_id=1, region_id=1, district_id=1
    )
    city_2_0_0_4 = CityModel(
        name="TestCity_4_0_0_1",
        country_id=2,
    )


class TestStreets(Values):
    street_1_0_0_1_1 = StreetModel(name="TestStreet_1_0_0_1_1", city_id=1)
    street_1_0_0_1_2 = StreetModel(name="TestStreet_1_0_0_1_2", city_id=1)
    street_1_1_1_3_3 = StreetModel(name="TestStreet_1_1_1_3_3", city_id=3)


class TestAddresses(Values):
    address_1_0_0_1_0_1 = AddressModel(building="123", city_id=1)
    address_1_0_0_1_0_2 = AddressModel(adds="near the lake", city_id=1)
    address_1_1_1_3_1_3 = AddressModel(
        building="666",
        adds="Behind the gate",
        office="13",
        city_id=3,
        street_id=3,
    )


@pytest.fixture(scope="module", autouse=True)
async def set_addresses(databases_and_migrations):
    """Set test addresses for the test database."""
    db = await anext(get_test_db())
    try:
        for table in TableNames:
            await db.execute(text(f"""TRUNCATE TABLE {table} CASCADE;"""))
        await db.commit()

        await TestCountries.to_db(db)
        assert (
            await db.scalar(select(func.count()).select_from(CountryModel))
        ) == 3, "problem with set into database countries"

        await TestRegions.to_db(db)
        assert (
            await db.scalar(select(func.count()).select_from(RegionModel))
        ) == 4, "problem with set into database Testregions"

        await TestDistricts.to_db(db)
        assert (
            await db.scalar(select(func.count()).select_from(DistrictModel))
        ) == 4, "problem with set into database districts"

        await TestCities.to_db(db)
        assert (
            await db.scalar(select(func.count()).select_from(CityModel))
        ) == 4, "problem with set into database cities"

        await TestStreets.to_db(db)
        assert (
            await db.scalar(select(func.count()).select_from(StreetModel))
        ) == 3, "problem with set into database districts"

        await TestAddresses.to_db(db)
        assert (
            await db.scalar(select(func.count()).select_from(AddressModel))
        ) == 3, "problem with set into database districts"
        await db.commit()

        yield

        for table in TableNames:
            await db.execute(text(f"""TRUNCATE TABLE {table} CASCADE;"""))
        await db.close()

    finally:
        await db.close()
