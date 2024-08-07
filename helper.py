from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI # type: ignore
from langchain_community.utilities.sql_database import SQLDatabase
from  openai import OpenAI
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from examples import example

import os

os.environ["OPENAI_API_KEY"] = "sk-proj-ap5XrDDS5KvlvlsxWWo8T3BlbkFJ0DXw0pRH0K3xzqrOFFxO"


from  openai import OpenAI
client = OpenAI()



client = OpenAI()


db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres", schema='lighthouse')


def query_validator_check(generate_query, llm):
    system = """Double check the user's {dialect} query for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins
    - Do not use an aggregate function (MAX) in a subquery where clause
    - Convert the necessary column into proper datatype to avoid the error
    - Keep in mind I am using Postgres SQL so the query should be suitable for Postgres SQL. Don't use any clause or function or keyword in the query that is not suitable for Postgre SQL

    If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

    Output the final SQL query only."""
    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{query}")]
    ).partial(dialect=db.dialect)
    validation_chain = prompt | llm | StrOutputParser()

    full_chain = {"query": generate_query} | validation_chain

    full_chain_updated = {"query": full_chain} | validation_chain

    return full_chain_updated

def get_few_shot_example(user_query):
    example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")

    example_selector = SemanticSimilarityExampleSelector.from_examples(
    example,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
    )

    # example_selector.select_examples({"input": user_query})

    prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
    suffix="User input: {input}\nSQL query: ",
    input_variables=["input", "top_k", "table_info"],
    )

    # formatted_prompt = prompt.format(input=user_query, top_k=3, table_info="lighthouse")

    return prompt


def code_prefix():
    """
    Code to prefix to the visualization code.
    """
    return """ 
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.figure_factory as ff
    import plotly.express as px 

    fig, ax = plt.subplot(figsize=(6.4, 2.4))
    """

def prepare_question(topic):
    """
    Code to prepare the question
    """

    # question_to_ask = f""""
    # You are expert in visualization using streamlit for any kind of topic. Generate a streamlit code(The script should only include code not comments), to create a visualization  that displays data for a given topic. 
    # The type of plot should be determined based on the topic provided. I will provide you the base streamlit code you need to return the complete code. The plot should be a colorfull plote 
    # so that it should be nice to visalize and also there should be proper ticker for x and y axis for easy to understand

    # For example, if the topic is 'Top 5 departments with the highest average salaries', a bar chart would be appropriate. 
    # The code should be flexible to handle different topics and data structures. The output should only contain the python code nothing else.

    # The topic for the visuzlization is - {topic}

    # Base Streamlit Code - {code_prefix()}
    # """
    question_to_ask = f"""
    You are an expert in visualization using Streamlit. Generate a Streamlit script that displays data for a specific topic, choosing the appropriate type of plot based on the topic. The code should be dynamic enough to handle various topics and data structures, and it should include only the Python code without comments.

    Steps for generating the code:
    1. Analyze the topic to understand the required visualization.
    2. Select the most suitable visualization type for the topic.
    3. Generate the complete Streamlit code using the provided base code.
    4. Generate the code based on the required library I have used in the Base Streamlit Code. Don't use any other library that is not used in the Base Streamlit Code.
    5. The response should contain only code and nothing else.
    

    Topic for visualization: {topic}
    Base Streamlit Code: {code_prefix()}
    """
    return question_to_ask

def prepare_postgres_question():
    answer_prompt = PromptTemplate.from_template(
    """You are an postgres SQL expert, you are expert in all kind of joins in postgres SQL. Given the following user question, corrosponding SQL query, and SQL result, answer the user question.
    
    

    Question: {question} 
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )

    return answer_prompt


def get_answer(user_query):
    sql_examples = get_few_shot_example(user_query)

    # db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:sourodip@localhost:5432/postgres", schema='lighthouse')
    print(sql_examples)
    answer_prompt = prepare_postgres_question()
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    generate_query = create_sql_query_chain(llm, db, sql_examples)
    execute_query = QuerySQLDataBaseTool(db=db)

    generate_query_chain = query_validator_check(generate_query, llm)

    rephrase_answer = answer_prompt | llm | StrOutputParser()

    chain = (
    RunnablePassthrough.assign(query=generate_query_chain).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )
    # breakpoint()
    # user_query_updted = user_query +' ' + "A note for you is - I am using postgres. So your response to the question should only contain query that is suitable for postgres"
    
    topic = chain.invoke({"question": f"{user_query}"})

    return topic


def get_code(topic):

    # topic = get_answer(user_query)
    # breakpoint()
    question_to_ask = prepare_question(topic)
    breakpoint()
    stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": question_to_ask}],
    # stream=True,
    )

    reply_content = stream.choices[0].message.content
    return reply_content


# question="What are the top 5 departments with the highest average salary?"

# code = get_code(question)
# breakpoint()