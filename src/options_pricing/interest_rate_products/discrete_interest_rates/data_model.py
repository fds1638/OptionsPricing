from pydantic import BaseModel
from pandantic import Pandantic

class LaggedSeries(BaseModel):
    lagged_values: float

class DeltaSeries(BaseModel):
    delta_values: float

class CoxIngersollRossX(BaseModel):
    lagged_values: float
    constant_values: float

class Validator():

    @staticmethod
    def validate_lagged_series(df, err="raise"):
        lagged_validator = Pandantic(LaggedSeries)
        lagged_validator.validate(dataframe=df, errors=err)

    @staticmethod
    def validate_delta_series(df, err="raise"):
        delta_validator = Pandantic(DeltaSeries)
        delta_validator.validate(dataframe=df, errors=err)

    @staticmethod
    def validate_c_i_r_X(df, err="raise"):
        c_i_r_validator = Pandantic(CoxIngersollRossX)
        c_i_r_validator.validate(dataframe=df, errors=err)
