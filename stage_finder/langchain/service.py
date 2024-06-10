from typing import Type

from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool

from pydantic import BaseModel
from sqlalchemy import text, create_engine

from stage_finder.models import SQLQueryInputs, SQLQueryValidatorInput, SQLQueryExecutorInput
from stage_finder.settings import OPENAI_API_KEY, DATABASE_URL
from stage_finder.utils import return_string_from_table

agent = None

system_message = SystemMessage(
    content="""You are support Q&A bot optimized for SQL query generation. If you are unable to answer specific user 
    query you are free to respond with 'I dont know'.

    Please make sure you complete the objective above with the following rules: 
    1/ Your job is to first breakdown your execution plan using available tools. Every tool may or may not be required 
    to complete task. Available tools are SQL query generator, SQL query validator, SQL query executor and response 
    generator. 
    2/ You should use the SQL validator and SQL executor tools if you decided to use SQL generator tool. 
    3/ Use response generator tool."""
)


class SQLqueryGeneratorTool(BaseTool):
    name = "sql-generator-tool"
    description = "SQL code generation tool. Useful when wants to generate SQL code from given user question."
    args_schema: Type[BaseModel] = SQLQueryInputs

    def _run(self, question: str):
        template = f"""
        You are a supportive Q&A bot. Below you have given user question your task is to convert that into SQL code.
        table schema: {return_string_from_table("business_index")}
        Question: {question}
        """
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_API_KEY)
        return llm.invoke(input=template)

    def _arun(self, url: str):
        raise NotImplementedError("error here")


class SQLQueryValidatorTool(BaseTool):
    name = "sql-query-validator-tool"
    description = "SQL code validation tool. Useful when wants to validate SQL code."
    args_schema: Type[BaseModel] = SQLQueryValidatorInput

    def _run(self, sql_code: str):
        template = f""" You are supportive query validator your task is to validate and return answers based on below 
        steps given llm agent responses. - Should return SQL code ONLY.

        Ex: LLM agent response: The SQL query to find the total number of employees is:
        
        ```sql
        SELECT COUNT(DISTINCT employee_id) AS total_employees
        FROM employee_usage_details;
        ```
        
        Response should be: SELECT COUNT(DISTINCT employee_id) AS total_employees
        FROM employee_usage_details;
        
        LLM Generated Response: {sql_code}
        """
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_API_KEY)
        return llm.invoke(input=template), sql_code

    def _arun(self, url: str):
        raise NotImplementedError("error here")


class SQLQueryExecutorTool(BaseTool):
    name = "sql-query-executor-tool"
    description = "SQL code executor tool. Useful when wants to execute SQL code."
    args_schema: Type[BaseModel] = SQLQueryExecutorInput

    def _run(self, sql_code: str, original_question: str):
        engine = create_engine(DATABASE_URL)

        result = engine.connect().execute(text(sql_code)).fetchall()
        return {"Executor Result": result, "Unprocessed LLM response": original_question}

    def _arun(self, url: str):
        raise NotImplementedError("error here")


if OPENAI_API_KEY:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_API_KEY)

    agent_kwargs = {
        "system_message": system_message,
    }

    tools = [
        SQLqueryGeneratorTool(),
        SQLQueryValidatorTool(),
        SQLQueryExecutorTool()
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
    )
