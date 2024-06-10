from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class ResponseTypes(Enum):
    QUESTION = "question"
    ANSWER = "answer"
    STATE_CHANGE = "state-change"
    ERROR = "error"


class StateChange(BaseModel):
    param: str
    value: str


class ServerResponse(BaseModel):
    response_type: ResponseTypes
    message: Optional[str]
    change: List[StateChange] = []

class SQLQueryInputs(BaseModel):
    """Inputs for SQLqueryGeneratorTool"""
    question: str = Field(description="User question to be convert into SQL query")

class SQLQueryValidatorInput(BaseModel):
    """Inputs for SQLQueryValidator tool"""
    sql_code: str = Field(description="LLM Agent generated response")

class SQLQueryExecutorInput(BaseModel):
    """Inputs for SQLQueryExecutorInput tool"""
    sql_code: str = Field(description="SQL Code to be executed.")
    original_question: str = Field(description="Unprocessed agent response to finalize end result.")

