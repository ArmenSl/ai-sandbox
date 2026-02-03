from datetime import datetime, date, time
from typing import List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator

from abc import ABC, abstractmethod

############################################
# Enumerations are defined here
############################################

class LicensingType(Enum):
    Open_Source = "Open_Source"
    Proprietary = "Proprietary"

class DatasetType(Enum):
    Test = "Test"
    Training = "Training"
    Validation = "Validation"

class EvaluationStatus(Enum):
    Processing = "Processing"
    Pending = "Pending"
    Done = "Done"
    Custom = "Custom"
    Archived = "Archived"

class ProjectStatus(Enum):
    Ready = "Ready"
    Archived = "Archived"
    Closed = "Closed"
    Created = "Created"
    Pending = "Pending"

############################################
# Classes are defined here
############################################
class CommentsCreate(BaseModel):
    Name: str
    TimeStamp: datetime
    Comments: str


class LegalRequirementCreate(BaseModel):
    standard: str
    legal_ref: str
    principle: str
    project_1: int  # N:1 Relationship (mandatory)


class ToolCreate(BaseModel):
    version: str
    licensing: LicensingType
    name: str
    source: str
    observation_1: Optional[List[int]] = None  # 1:N Relationship


class DatashapeCreate(BaseModel):
    accepted_target_values: str
    f_date: Optional[List[int]] = None  # 1:N Relationship
    f_features: Optional[List[int]] = None  # 1:N Relationship
    dataset_1: Optional[List[int]] = None  # 1:N Relationship


class ProjectCreate(BaseModel):
    status: ProjectStatus
    name: str
    legal_requirements: Optional[List[int]] = None  # 1:N Relationship
    involves: Optional[List[int]] = None  # 1:N Relationship
    eval: Optional[List[int]] = None  # 1:N Relationship


class EvaluationCreate(BaseModel):
    status: EvaluationStatus
    ref: List[int]  # N:M Relationship
    config: int  # N:1 Relationship (mandatory)
    project: int  # N:1 Relationship (mandatory)
    observations: Optional[List[int]] = None  # 1:N Relationship
    evaluates: List[int]  # N:M Relationship


class MeasureCreate(BaseModel):
    value: float
    uncertainty: float
    unit: str
    error: str
    measurand: int  # N:1 Relationship (mandatory)
    observation: int  # N:1 Relationship (mandatory)
    metric: int  # N:1 Relationship (mandatory)


class AssessmentElementCreate(ABC, BaseModel):
    name: str
    description: str


class ConfigurationCreate(AssessmentElementCreate):
    params: Optional[List[int]] = None  # 1:N Relationship
    eval: Optional[List[int]] = None  # 1:N Relationship


class ElementCreate(AssessmentElementCreate):
    measure: Optional[List[int]] = None  # 1:N Relationship
    project: Optional[int] = None  # N:1 Relationship (optional)
    evalu: List[int]  # N:M Relationship
    eval: List[int]  # N:M Relationship


class ModelCreate(ElementCreate):
    pid: str
    source: str
    licensing: LicensingType
    data: str
    dataset: int  # N:1 Relationship (mandatory)


class DatasetCreate(ElementCreate):
    version: str
    licensing: LicensingType
    dataset_type: DatasetType
    source: str
    observation_2: Optional[List[int]] = None  # 1:N Relationship
    models: Optional[List[int]] = None  # 1:N Relationship
    datashape: int  # N:1 Relationship (mandatory)


class FeatureCreate(ElementCreate):
    min_value: float
    max_value: float
    feature_type: str
    date: int  # N:1 Relationship (mandatory)
    features: int  # N:1 Relationship (mandatory)


class ObservationCreate(AssessmentElementCreate):
    whenObserved: datetime
    observer: str
    eval: int  # N:1 Relationship (mandatory)
    dataset: int  # N:1 Relationship (mandatory)
    tool: int  # N:1 Relationship (mandatory)
    measures: Optional[List[int]] = None  # 1:N Relationship


class ConfParamCreate(AssessmentElementCreate):
    param_type: str
    value: str
    conf: int  # N:1 Relationship (mandatory)


class MetricCreate(AssessmentElementCreate):
    category: List[int]  # N:M Relationship
    derivedBy: List[int]  # N:M Relationship
    measures: Optional[List[int]] = None  # 1:N Relationship


class DerivedCreate(MetricCreate):
    expression: str
    baseMetric: List[int]  # N:M Relationship


class DirectCreate(MetricCreate):
    pass


class MetricCategoryCreate(AssessmentElementCreate):
    metrics: List[int]  # N:M Relationship


