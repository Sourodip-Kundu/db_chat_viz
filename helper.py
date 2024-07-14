from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from  openai import OpenAI
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

import os

os.environ["OPENAI_API_KEY"] = ""


from  openai import OpenAI
client = OpenAI()



client = OpenAI()


db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:sourodip@localhost:5432/postgres", schema='employees')



def code_prefix():
    """
    Code to prefix to the visualization code.
    """
    return """ 
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt 

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
    4. The response should contain only code and nothing else.

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
    db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:sourodip@localhost:5432/postgres", schema='employees')
    answer_prompt = prepare_postgres_question()
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    generate_query = create_sql_query_chain(llm, db)
    execute_query = QuerySQLDataBaseTool(db=db)

    rephrase_answer = answer_prompt | llm | StrOutputParser()

    chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )
    # breakpoint()
    user_query_updted = user_query +' ' + "A note for you is - I am using postgres. So your response to the question should only contain query that is suitable for postgres"

    topic = chain.invoke({"question": f"{user_query_updted}"})

    return topic


def get_code(topic):

    # topic = get_answer(user_query)
    # breakpoint()
    question_to_ask = prepare_question(topic)

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