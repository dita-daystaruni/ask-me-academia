import PyPDF2
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import List

load_dotenv()

class SingleQuestion(BaseModel):
    question: str = Field(
        title="Question",
        description="question from the lecture notes",
    )
    answer: str = Field(
        title="binary answer",
        description="answer to the question in True or False",
    )


class BinaryOutput(BaseModel):
    """Model to capture LLM response with questions and answers."""
    questions: List[SingleQuestion] = Field(
        title="Questions and Answers",
        description="List of dictionary with  QanaA generated the notes"
    )
        
class MultiQuestion(BaseModel):
    question: str = Field(
        title="Question",
        description="Question text",
    )
    multiple_choice: List[str] = Field(
        title="Multiple Choice",
        description="List of multiple choice answers",
    )
    correct_answer: str = Field(
        title="correct answer",
        description="Answer text",
    )

class MultiOutput(BaseModel):
    questions: List[MultiQuestion] = Field(
        title="Questions and Answers",
        description="List of questions, choices and answers",
    )

    
SystemMessage = """
You are a diligent and thorough study assistant for university students. Your task is to review lecture notes uploaded by students, understand the topic covered, and generate 10  questions and answers based on the notes for quick revision. The questions should be related to the topic and should help the student review the material effectively. 
"""


# model = ChatGroq(
#     temperature=0,
#     model="llama3-70b-8192",
#     api_key=os.getenv("GROQ_API_KEY"),
# ).with_structured_output(Response)


binaryParser = JsonOutputParser(pydantic_object=BinaryOutput)
multiParser = JsonOutputParser(pydantic_object=MultiOutput)

openai_binary_function = [convert_to_openai_function(BinaryOutput)]
openai_multi_function = [convert_to_openai_function(MultiOutput)]

model = ChatOpenAI(
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
)



def process_pdf(file):
    """
    Reads a PDF file, checks if it's text-based, and returns the text content.

    Args:
        file (file-like object): The PDF file.

    Returns:
        str or None: The text content of the PDF if successful, or None if the PDF isn't text-based or an error occurs.
    """
    try:
        reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()

        if not pdf_text.strip():
            print("Error: The PDF does not contain extractable text.")
            return None

        return pdf_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

human_text_bianry = """
### out put instaction ###
- The system should generate 10 questions and answers based on the lecture notes.
- The questions should be in true or false format.
- The format of the output should be in the format bellow:
    {{"questions":[
        {{"Question1": "Answer1"}},
        {{"Question2": "Answer2"}}
        ...]}}
    
bellow are the attached notes:
{text}   
"""

human_text_multi_choice = """
### out put instaction ###
- The system should generate 10 questions and answers based on the lecture notes.
- The questions should be in the format bello:
    {{questions:[
        q1: 
        {{question: What is the capital of Nigeria?,}}
        {{multiple_choice: ["Abuja", "Lagos", "Kano", "Ibadan"],}}
        {{correct answer: Abuja.}},
        ...,
        qn:
        {{question: What is ...?,}}
        {{multiple_choice: ["answer1", "answer2", "answer3", "answer4"],}}
        {{correct answer : answer.}}
    ]}}
        
bellow are the attached notes:
{text}  
"""


def get_questions_and_answers(text, multiple_choice=True):
    max_context_length = 8000
    current_length = len(text.split())
    
    human_text = human_text_multi_choice if multiple_choice else human_text_bianry
    
    if current_length > max_context_length:
        text = " ".join(text.split()[:max_context_length])
        
    try:
        if multiple_choice:
            #use the multi choice model
            prompt = ChatPromptTemplate.from_messages([("system", SystemMessage), ("human", human_text)])
            chain = prompt | model | multiParser
            results = chain.invoke({"text": text})
            # results
            return results
        else:
            #use the binary model
            prompt = ChatPromptTemplate.from_messages([("system", SystemMessage), ("human", human_text)])
            chain = prompt | model | binaryParser
            results = chain.invoke({"text": text})
            return results

    except Exception as e:
        raise e
