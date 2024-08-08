from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import json
import traceback

class LLmGradingService:
    def __init__(self) -> None:
        self.llm = ChatOllama(model="llama3", temperature=0.2)

    async def grade_resume(self, candidate_context, job_context) -> str:
        try:
            # Define the response schemas
            response_schemas = [
                ResponseSchema(name="summary", description="A summary of the evaluation"),
                ResponseSchema(name="grade", description="The grade as an integer from 1 to 10")
            ]

            # Create the output parser
            output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

            # Get the format instructions
            format_instructions = output_parser.get_format_instructions()

            PROMPT_TEMPLATE = """
            You are an expert in evaluating resumes. Your task is to grade the candidate's resume based on the provided job context. Please follow these steps:

            1. Analyze the Job Context: Identify the key skills, experiences, years of experience and qualifications required for the job. Job Context: {job_context}
            2. Evaluate the Candidate's Resume: Compare the candidate's qualifications against the job context. Candidate Context: {candidate_context}
            3. Consider that the organization is looking for a candidate who works on innovative projects and has experience in the latest technologies. 
            4. Assign a Grade: Rate the resume on a scale from 1 to 10, where 1 is poor and 10 is excellent.
            5. Provide Justification: Explain the reasoning behind the assigned grade, detailing strengths and weaknesses.
            6. Candidate should be rated based on their qualifications, experience, innovative behavior, qualities and relevance to the job context.
            7. Candidate rating should indicate this 1-4: Poor with 30% match, 5-6: Average with 50% match, 7-8: Good with 70% match, 9-10: Excellent with a 90% match.
            8. Check to confirm if the candidate's resume looks like it's generated by AI by checking for unnatural language.

            {format_instructions}
            """

            # Create the prompt template
            system_prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

            # Format the prompt with all required variables
            system_prompt = system_prompt_template.format(
                job_context=job_context,
                candidate_context=candidate_context,
                format_instructions=format_instructions
            )

            # Get the response from the LLM
            response = self.llm.invoke(system_prompt)

            # Parse the output
            parsed_output = output_parser.parse(response.content)
            return parsed_output

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            raise e