import PyPDF2
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

class Response(BaseModel):
    """Model to capture LLM response with questions and answers."""
    questions_and_answers: list[dict[str, str]] = Field(
        title="Questions and Answers",
        description="List of generated true or false questions with their answers"
    )
    
    
SystemMessage = """
You are a diligent and thorough study assistant for university students. Your task is to review lecture notes uploaded by students, understand the topic covered, and generate 10 true or false questions based on the notes for quick revision. The questions should be related to the topic and should help the student review the material effectively. Each question should be followed by its correct answer, either 'True' or 'False'.
"""


model = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
).with_structured_output(Response)

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

def get_questions_and_answers(text):
    try:
        prompt = ChatPromptTemplate.from_messages([("system", SystemMessage), ("human", text)])
        chain = prompt | model
        results = chain.invoke({"text": ""})
        return results

    except Exception as e:
        print(e)
        return None
