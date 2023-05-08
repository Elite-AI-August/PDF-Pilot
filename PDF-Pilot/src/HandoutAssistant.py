
"""
HandoutAssistant.py

This file contains the HandoutAssistant class which is designed to process PDF handouts and answer questions based on their content. 

The HandoutAssistant class is responsible for:

1. Converting PDF to text.
2. Segmenting the text using AI21 Studio's API.
3. Loading the segmented questions.
4. Identifying relevant segments based on user questions using Hugging Face's Transformers.
5. Generating a prompt for OpenAI's GPT-3.
6. Extracting answers and segment IDs from GPT-3's response.

The file also contains a PDFHandler class that is responsible for highlighting relevant segments in the input PDF.
"""


import os
import fitz
import json
import requests
from transformers import pipeline
import openai
import re


class NLP:
    def __init__(self):
        self.pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    def get_response(self, user_question, context):
        return self.pipeline(question=user_question, context=context)


class PDFHandler:
    @staticmethod
    def pdf_to_text(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        page_texts = []
        for page in doc:
            page_text = page.get_text("text")
            text += page_text
            page_texts.append({"text": page_text, "page_number": page.number})
        return text, page_texts

    @staticmethod
    def highlight_text(input_pdf, output_pdf, text_to_highlight):
        phrases = text_to_highlight.split('\n')
        with fitz.open(input_pdf) as doc:
            for page in doc:
                for phrase in phrases:
                    areas = page.search_for(phrase)
                    if areas:
                        for area in areas:
                            highlight = page.add_highlight_annot(area)
                            highlight.update()
            doc.save(output_pdf)


class AI21Segmentation:
    @staticmethod
    def segment_text(text):
        url = "https://api.ai21.com/studio/v1/segmentation"
        payload = {
            "sourceType": "TEXT",
            "source": text
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {os.environ['AI21_API_KEY']}"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("segments")
        else:
            print(f"An error occurred: {response.status_code}")
            return None


class OpenAIAPI:
    def __init__(self):
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def get_answer_and_id(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer_text = response.choices[0].text.strip()
        lines = response.choices[0].text.strip().split('\n')
        answer = lines[0].strip()
        answer = answer.replace("Answer:", "").strip()
        try:
            segment_id = int(re.search(r'<ID: (\d+)>', answer).group(1))
            answer = re.sub(r'<ID: \d+>', '', answer).strip()
        except AttributeError:
            segment_id = None
        return answer, segment_id

class HandoutAssistant:
    def __init__(self):
        self.nlp = NLP()
        self.openai_api = OpenAIAPI()
        self.current_pdf_path = None
        self.questions_data = None

    def process_pdf(self, pdf_path):
        text, page_texts = PDFHandler.pdf_to_text(pdf_path)
        segmented_text = AI21Segmentation.segment_text(text)
        questions_data = self.assign_page_numbers_and_ids_to_segments(segmented_text, page_texts)
        return questions_data

    def assign_page_numbers_and_ids_to_segments(self, segmented_text, page_texts):
        for idx, segment in enumerate(segmented_text):
            segment_text = segment["segmentText"]
            segment["id"] = idx + 1
            max_overlap = 0
            max_overlap_page_number = None
            for page_text in page_texts:
                overlap = len(set(segment_text.split()).intersection(set(page_text["text"].split())))
                if overlap > max_overlap:
                    max_overlap = overlap
                    max_overlap_page_number = page_text["page_number"]
            segment["page_number"] = max_overlap_page_number + 1
            print(f"Element ID: {segment['id']}, Page Number: {segment['page_number']}")

        return segmented_text

    def get_relevant_segments(self, questions_data, user_question):
        relevant_segments = []
        for question_data in questions_data:
            context = question_data["segmentText"]
            response = self.nlp.get_response(user_question, context)
            if response["score"] > 0.5:
                first_occurrence_page_number = question_data.get("page_number", 1)
                relevant_segments.append({
                    "id": question_data["id"],
                    "segment_text": context,
                    "score": response["score"],
                    "page_number": first_occurrence_page_number
                })
        relevant_segments.sort(key=lambda x: x["score"], reverse=True)
        return relevant_segments[:10]

    def generate_prompt(self, question, relevant_segments):
        
        prompt = f"""
You are an AI Q&A bot. You will be given a question and a list of relevant text segments with their IDs. Please provide an accurate and concise answer based on the information provided, or indicate if you cannot answer the question with the given information. Also, please include the ID of the segment that helped you the most in your answer by writing <ID: > followed by the ID number.

Question: {question}

Relevant Segments:"""

        for segment in relevant_segments:
            prompt += f'\n{segment["id"]}. "{segment["segment_text"]}"'
        return prompt

    def process_pdf_and_get_answer(self, pdf_path, question):
        if pdf_path != self.current_pdf_path:
            self.current_pdf_path = pdf_path
            self.questions_data = self.process_pdf(pdf_path)

        relevant_segments = self.get_relevant_segments(self.questions_data, question)

        if relevant_segments:
            prompt = self.generate_prompt(question, relevant_segments)
            openai_answer, segment_id = self.openai_api.get_answer_and_id(prompt)

            segment_data = next((seg for seg in relevant_segments if seg["id"] == segment_id), None)
            segment_text = segment_data["segment_text"] if segment_data else None
            page_number = segment_data["page_number"] if segment_data else None

            return openai_answer, segment_id, segment_text, page_number
        else:
            return None, None, None, None
