from datetime import date
from pydantic import BaseModel, Field

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ukrdc_sqla.ukrdc import Patient, PatientNumber, ProgramMembership

from radar_patient_check.demo import DEMO_PATIENTS_MAP

from .database import get_session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


class RadarCheckRequest(BaseModel):
    nhs_number: str = Field(
        ..., description="The patient's NHS number", alias="nhsNumber"
    )
    date_of_birth: date = Field(
        ..., description="The patient's date of birth", alias="dateOfBirth"
    )


class RadarCheckResponse(BaseModel):
    nhs_number: bool = Field(
        ...,
        description="NHS number matched against a known RADAR record",
        alias="nhsNumber",
    )
    date_of_birth: bool = Field(
        ...,
        description="Date of birth matched against a known RADAR record",
        alias="dateOfBirth",
    )

    class Config:
        allow_population_by_field_name = True


def api_key_auth(request_key: str = Depends(oauth2_scheme)):
    api_keys = settings.apikeys
    if not api_keys or (api_keys and request_key not in api_keys):
        raise HTTPException(status_code=401, detail="Forbidden")


@app.post(
    "/radar_check/",
    dependencies=[Depends(api_key_auth)],
    response_model=RadarCheckResponse,
)
async def radar_check(
    record: RadarCheckRequest, session=Depends(get_session)
) -> RadarCheckResponse:
    """
    Checks to see if an NHS number is linked to a Radar membership,
    and if the DoB provided matches that on file.

    Can return true for the NHS number and false for the DoB if the membership exists but DoB does not match.
    """

    # NOTE: Pylance (VS Code language server) struggles with this line as Pydantic aliases confuse it.
    #       It's fine to ignore the error.
    response = RadarCheckResponse(nhs_number=False, date_of_birth=False)  # type: ignore

    # Handle NHS demo patients
    if record.nhs_number in DEMO_PATIENTS_MAP:
        demo_patient = DEMO_PATIENTS_MAP[record.nhs_number]
        if demo_patient.is_radar_member:
            response.nhs_number = True
            response.date_of_birth = demo_patient.date_of_birth == record.date_of_birth

    # Handle real patients
    elif (
        patient_numbers := session.query(PatientNumber)
        .filter_by(patientid=record.nhs_number, numbertype="NI")
        .all()
    ):
        pids = [patient_number.pid for patient_number in patient_numbers]

        if (
            session.query(ProgramMembership)
            .filter(
                ProgramMembership.pid.in_(pids),
                ProgramMembership.program_name == "RADAR",
                ProgramMembership.to_time == None,
            )
            .first()
        ):
            response.nhs_number = True

            recorded_dobs = (
                session.query(Patient.birth_time).filter(Patient.pid.in_(pids)).all()
            )

            recorded_dobs = [
                recorded_dob.birth_time.date() for recorded_dob in recorded_dobs
            ]

            response.date_of_birth = record.date_of_birth in recorded_dobs

    return response
