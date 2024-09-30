import PyPDF2
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import List


class SingleQuestion(BaseModel):
    question: str = Field(
        title="Question",
        description="True or false question from the lecture notes",
    )
    answer: bool = Field(
        title="boolean answer",
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

binaryParser = JsonOutputParser(pydantic_object=BinaryOutput)
multiParser = JsonOutputParser(pydantic_object=MultiOutput)


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
{SystemMessage}

### out put instaction ###
- The system should generate 10 questions and answers based on the lecture notes.
- The question should be in True or False format. and the answer should be either True or False.
- The format of the output should be in the format bellow:
    {{"questions":[
        {{"Question": "Question1", "Answer": "True"}},
        {{"Question2": "Question2", "Answer":"False"}},
        ...]}}
        
    {format_instructions}
        
    
    
bellow are the attached notes:
{text}   
"""

human_text_multi_choice = """
{SystemMessage}

### out put instaction ###
- The system should generate 10 questions and answers based on the lecture notes.
- The questions should be in the format bello:
    {format_instructions}
        
bellow are the attached notes:
{text}  
"""


def get_muti_QnA(text):
    try:

        #use the multi choice model
        prompt = PromptTemplate(
                                template = human_text_multi_choice,
                                input_variables=['SystemMessage','text'],
                                partial_variables={"format_instructions": multiParser.get_format_instructions()}
                                )
        chain = prompt | model | multiParser
        results = chain.invoke({"SystemMessage":SystemMessage,"text": text,"format_instructions": multiParser.get_format_instructions()})
        return results
    except Exception as e:
        print(e)
        raise e
    
def get_binary_QnA(text):

    try:
        prompt = PromptTemplate(
                                template = human_text_bianry,
                                input_variables=['SystemMessage','text'],
                                partial_variables={"format_instructions": binaryParser.get_format_instructions()}
                                )
        chain = prompt | model | binaryParser
        results = chain.invoke({"SystemMessage":SystemMessage,"text": text,"format_instructions": binaryParser.get_format_instructions()})
        return results
    except Exception as e:
        print(e)
        raise e
    
    
    
def get_questions_and_answers(text,multi_choice):
    """
    Generates questions and answers from the text content of a PDF file.

    Args:
        text (str): The text content of the PDF file.
        multi_choice (bool): A boolean value indicating whether to generate multiple-choice questions.

    Returns:
        dict or None: A dictionary containing the questions and answers if successful, or None if an error occurs.
    """
    max_context_length = 8000
    current_length = len(text.split())
    
    if current_length > max_context_length:
        text = " ".join(text.split()[:max_context_length])
    
    try:
        if multi_choice:
            results = get_muti_QnA(text)
        else:
            results = get_binary_QnA(text)
        return results
    except Exception as e:
        print(f"Error generating questions and answers: {e}")
        return None