from pydantic import BaseModel, Field
from src.config import Limits
from src.core.enums import InstitutionType
from src.core.mixins import ShortHttpUrl
from src.geo import AddressScheme


class BaseInstitutionScheme(BaseModel):
    """The base schema for institution schemas.

    #### Attrs:
    - name (str):
        Institution name.
    - description (str | None):
        Institution description.
    - site (AnyHttpUrl | None):
        Institution web-site.
    - categories: list[InstitutionType]:
        Categories of institution.
    """

    name: str = Field(
        title="Name of institution",
        example="Broadwood Area School",
        min_length=Limits.MIN_LEN_PROVIDER_NAME,
        max_length=Limits.MAX_LEN_PROVIDER_NAME,
    )
    description: str | None = Field(
        default=None,
        title="Dscription of institution",
        example="Nau mai, haere mai ki Te Kura Takiwa o Manganuiowae. "
        "Our mission: 'Challenging  ourselves to reach our full potential'. "
        "Whakaara i te kākano",
        max_length=Limits.MAX_LEN_PROVIDER_DESCRIPTION,
    )
    site: ShortHttpUrl | None = Field(
        default=None,
        title="Web-site of institution",
        example="https://www.broadwood.school.nz/",
    )
    categories: list[InstitutionType] = Field(
        title="Categories of institution", example=[100, 201]
    )


class CreateInstitutionScheme(BaseInstitutionScheme):
    """The schema for create a new institution.

    #### Attrs:
    - name (str):
        Institution name.
    - description (str | None):
        Institution description.
    - site (AnyHttpUrl | None):
        Institution web-site.
    - categories: list[InstitutionType]:
        Categories of institution.
    - owner_id (int | None):
        Institution owner ID.
    - address (AddressScheme):
        Institution address.
    """

    owner_id: int | None = Field(default=None, title="Institution owner")
    address: AddressScheme = Field(
        title="Address of institution",
    )
