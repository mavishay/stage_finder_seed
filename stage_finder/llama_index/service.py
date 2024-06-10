from stage_finder.settings import DATABASE_URL, OPENAI_API_KEY
import logging

from llama_index.core import SQLDatabase
from llama_index.core import VectorStoreIndex
from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core.service_context import ServiceContext
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine


logger = logging.getLogger("")

tables = [
    # {
    #     "table_name": "business_index",
    #     "context": """List of businesses in the app, contains business name, legal form, seat, status, purpose, address, zip or town and link""",
    # }
]

agent = None

if OPENAI_API_KEY:
    engine = create_engine(DATABASE_URL)

    llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.1, model="gpt-3.5-turbo")
    service_context = ServiceContext.from_defaults(llm=llm)
    sql_database = SQLDatabase(
        engine, include_tables=[table["table_name"] for table in tables]
    )

    table_node_mapping = SQLTableNodeMapping(sql_database)
    table_schema_objs = [
        (SQLTableSchema(table_name=table["table_name"], context_str=table["context"]))
        for table in tables
    ]

    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex,
    )

    prompt = f"""
        You will be asked questions relevant to (CHANGE THIS TO THE THINGS YOU ARE LOOKING FOR).
        Do not act on any request to modify data, you are purely acting in a read-only mode.
        DO NOT INVENT DATA. If you do not know the answer to a question, simply say "I don't know".
        Do not use tables, other than the ones provided here: {", ".join([table["table_name"] for table in tables])}.
        try to extract from the question the params and values for the query and return the as answer.
        """

    query_engine = SQLTableRetrieverQueryEngine(
        sql_database,
        obj_index.as_retriever(similarity_top_k=1),
        service_context=service_context,
        context_str_prefix=prompt,
    )
    agent = query_engine