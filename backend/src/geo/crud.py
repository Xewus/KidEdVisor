from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import CRUD

from .models import (
    AddressModel,
    CityModel,
    CountryModel,
    DistrictModel,
    PhoneModel,
    RegionModel,
    StreetModel,
)
from .shemes import AddressScheme
from .utils import FullAddress, get_valid_address


class PhoneCRUD(CRUD):
    """The set of `CRUD` operations for `AddressModel`.

    #### Methods:
    - save: tuple[Base, None] | tuple[None, str]
    - create: tuple[Base, None] | tuple[None, str]
    - get_many: list[Base]
    - get: Base | None
    - update: tuple[Base, None] | tuple[None, str]
    """


class AddressCRUD(CRUD):
    """The set of `CRUD` operations for `AddressModel`.

    #### Methods:
    - save: tuple[Base, None] | tuple[None, str]
    - create: tuple[Base, None] | tuple[None, str]
    - get_many: list[Base]
    - get: Base | None
    - update: tuple[Base, None] | tuple[None, str]
    - get_full_address:  FullAddress | None
    - flush_new_address: FullAddress
    """

    model: AddressModel

    async def __set_region(
        self,
        db: AsyncSession,
        exist_address: FullAddress,
        valid_address: AddressScheme,
    ) -> None:
        """Set valid region to `FullAddress` and flush it to the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - exist_address (FullAddress):
            Address from the database with all related data.
        - valid_address (AddressScheme):
            Valid address from another API.
        """
        if not exist_address.region and valid_address.region:
            exist_address.region: RegionModel = RegionModel(
                name=valid_address.region,
                country_id=exist_address.country.id,
            )
            db.add(exist_address.region)
            await db.flush((exist_address.region,))

    async def __set_district(
        self,
        db: AsyncSession,
        exist_address: FullAddress,
        valid_address: AddressScheme,
    ) -> None:
        """Set valid district to `FullAddress` and flush it to the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - exist_address (FullAddress):
            Address from the database with all related data.
        - valid_address (AddressScheme):
            Valid address from another API.
        """
        if not exist_address.district and valid_address.district:
            exist_address.district: DistrictModel = DistrictModel(
                name=valid_address.district
            )
            if exist_address.region:
                exist_address.district.region_id = exist_address.region.id
            db.add(exist_address.district)
            await db.flush((exist_address.district,))

    async def __set_city(
        self,
        db: AsyncSession,
        exist_address: FullAddress,
        valid_address: AddressScheme,
    ) -> None:
        """Set valid city to `FullAddress` and flush it to the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - exist_address (FullAddress):
            Address from the database with all related data.
        - valid_address (AddressScheme):
            Valid address from another API.
        """
        if not exist_address.city and valid_address.city:
            exist_address.city: CityModel = CityModel(
                name=valid_address.city, country_id=exist_address.country.id
            )
            if exist_address.region:
                exist_address.city.region_id = exist_address.region.id
            if exist_address.district:
                exist_address.city.district_id = exist_address.district.id
            db.add(exist_address.city)
            await db.flush((exist_address.city,))

    async def __set_street(
        self,
        db: AsyncSession,
        exist_address: FullAddress,
        valid_address: AddressScheme,
    ) -> None:
        """Set valid street to `FullAddress` and flush it to the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - exist_address (FullAddress):
            Address from the database with all related data.
        - valid_address (AddressScheme):
            Valid address from another API.
        """
        if not exist_address.street and valid_address.street:
            exist_address.street: StreetModel = StreetModel(
                name=valid_address.street,
                city_id=exist_address.city.id,
            )
            db.add(exist_address.street)
            await db.flush((exist_address.street,))

    async def get_full_address(
        self,
        db: AsyncSession,
        address: AddressScheme,
    ) -> FullAddress:
        """Get an address with all related data.

        If the address is not found,
        all response instance attributes will be empty.
        If no larger objects are found,
        then smaller objects should contain `None`.
        INFO: if a city can be without a region or district,
        then it can be found without them.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - address (AddressScheme):
            Data to search.

        #### Returns:
        - FullAddress:
            Address with all related data.
        """
        select_tables = (
            CountryModel,
            RegionModel if address.region else None,
            DistrictModel if address.district else None,
            CityModel if address.city else None,
            StreetModel if address.street else None,
            AddressModel if address.building or address.adds else None,
        )
        stmt = select(*select_tables).select_from(CountryModel)

        if address.region:
            stmt = stmt.outerjoin(
                RegionModel,
                and_(
                    RegionModel.country_id == CountryModel.id,
                    RegionModel.name == address.region,
                ),
            )

        if address.district:
            stmt = stmt.outerjoin(
                DistrictModel,
                and_(
                    DistrictModel.region_id == RegionModel.id,
                    DistrictModel.name == address.district,
                ),
            )

        if address.city:
            join_on = [
                CityModel.country_id == CountryModel.id,
                CityModel.name == address.city,
            ]
            if address.region:
                join_on.append(CityModel.region_id == RegionModel.id)
            if address.district:
                join_on.append(CityModel.district_id == DistrictModel.id)
            stmt = stmt.outerjoin(
                CityModel,
                and_(*join_on),
            )

        if address.street:
            stmt = stmt.outerjoin(
                StreetModel,
                and_(
                    StreetModel.city_id == CityModel.id,
                    StreetModel.name == address.street,
                ),
            ).outerjoin(
                AddressModel,
                and_(
                    AddressModel.city_id == CityModel.id,
                    AddressModel.street_id == StreetModel.id,
                    AddressModel.building == address.building,
                    AddressModel.adds == address.adds,
                    AddressModel.office == address.office,
                ),
            )
        else:
            stmt = stmt.outerjoin(
                AddressModel,
                and_(
                    AddressModel.city_id == CityModel.id,
                    AddressModel.building == address.building,
                    AddressModel.adds == address.adds,
                    AddressModel.office == address.office,
                ),
            )

        stmt = stmt.where(CountryModel.name == address.country)
        return FullAddress(*(await db.execute(stmt)).first())

    async def flush_new_address(
        self,
        db: AsyncSession,
        new_address: AddressScheme,
        exist_address: FullAddress,
    ) -> FullAddress:
        """Get valid data using user input and flush it to the database.

        ATTENTION: You must use `commit()` yourself to save it,
         otherwise the new data will be erased by the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - new_address (AddressScheme):
            User-entered data.
        - exist_address (FullAddress):
            Data retrieved from database.

        #### Returns:
        - FullAddress:
            Data flushed into the database.
        """
        valid_address = await get_valid_address(new_address)

        if new_address != valid_address:
            exist_address = await self.get_full_address(db, valid_address)
            if exist_address.address:
                return exist_address

        await self.__set_region(db, exist_address, valid_address)
        await self.__set_district(db, exist_address, valid_address)
        await self.__set_city(db, exist_address, valid_address)
        await self.__set_street(db, exist_address, valid_address)

        exist_address.address = AddressModel(
            city_id=exist_address.city.id,
            street_id=exist_address.street.id,
            building=new_address.building,
            adds=new_address.adds,
            office=new_address.office,
        )
        db.add(exist_address.address)
        await db.flush((exist_address.address,))
        db.add_all(
            (
                PhoneModel(number=number, address_id=exist_address.address.id)
                for number in new_address.phones
            )
        )
        await db.flush()
        return exist_address


address_crud = AddressCRUD(AddressModel)
phone_crud = PhoneCRUD(PhoneModel)
