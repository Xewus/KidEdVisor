from pydantic import AnyHttpUrl, BaseModel, Field

from src.config import Limits
from src.core.enums import InstitutionType


class BaseInstitutionScheme(BaseModel):
    name: str = Field(
        title="Name of institution",
        example="Harvard University",
        max_length=Limits.MAX_LEN_PROVIDER_NAME,
    )
    description: str | None = Field(
        default=None,
        title="Dscription of institution",
        example="With world-class faculty, "
        "groundbreaking research opportunities, and "
        "a diverse group of talented students, "
        "Harvard is more than just a place to get an education.",
        max_length=Limits.MAX_LEN_PROVIDER_DESCRIPTION,
    )
    address: str = Field(
        title="Address of institution",
        example="Cambridge, Massachusetts, United States",
    )
    site: AnyHttpUrl | None = Field(
        default=None,
        title="Web-site of institution",
        example="https://www.harvard.edu/",
    )
    categories: list[InstitutionType] = Field(
        title="Categories of institution", example=[100, 201]
    )
