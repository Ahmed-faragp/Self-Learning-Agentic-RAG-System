

from openai import OpenAI
import os

from chroma_vdb import retrieve_with_confidence, add_document_to_chroma
from memory import conversation , save_memory_to_file, load_memory_from_file, get_memory_messages
from prompt_sys import generate_prompt,learning_template
from dotenv import load_dotenv
from routing import classify_intent

import warnings
warnings.filterwarnings("ignore")


load_dotenv() 
api_key = os.getenv("OPENROUTER_API_KEY")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key)




# def ask_question(question):
#     load_memory_from_file()
#     context, is_confident = retrieve_with_confidence(question)
#     if not is_confident:
#         print("""
#               I don't know this function yet, please teach me by providing 
#               1. code
#               2. explanation
#               3. function name
              
#               """)
#         function_name = input("function name:\n")
#         code = multiline_input()
#         explanation = input("explanation:\n")
#         add_document_to_chroma(function_name, code, explanation)
    
#     else:
#         context = "\n\n".join(context)
#         mode = classify_intent(question)
#         memory_summary = conversation.memory.buffer
#         prompt = generate_prompt(mode, question, context, memory_summary)
#         memory_messages = get_memory_messages()
#         messages = memory_messages + prompt
#         response = client.chat.completions.create(
#             model="meta-llama/llama-3-8b-instruct", 
#             messages=messages
#             )
#         conversation.memory.save_context({"input": question}, {"output": response.choices[0].message.content})
#         save_memory_to_file()
#         return response.choices[0].message.content
        
    
user_question = "How do I reverse a linked list in Python?"

    



 




