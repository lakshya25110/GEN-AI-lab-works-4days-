from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List

class Generator:
    def __init__(self, api_key: str, model_name: str = "llama3-8b-8192"):
        self.llm = ChatGroq(
            api_key=api_key,
            model_name=model_name,
            temperature=0
        )
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert technical assistant. Use the provided context to answer the user question.
        If the answer is not in the context, say that you don't know based on the provided manual.
        Do not make up information.
        
        Context:
        {context}
        
        Question: 
        {question}
        
        Answer:
        """)
        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        context_text = "\n\n".join(context_chunks)
        response = self.chain.invoke({
            "context": context_text,
            "question": question
        })
        return response
