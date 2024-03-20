import requests
import json
import os

class ChatGPTHelper:
    __openai_api_key = None # put yout api key here
    __url = "https://api.openai.com/v1/chat/completions"

    __headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {__openai_api_key}"
    }


    def check_api_key(self):
        if self.__openai_api_key is None:
            raise ValueError("OpenAI API key is not set in environment variables.")

    
    def get_hint_from_chatgpt(self, question : str):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Give a short hint that will help to the user who answers this question without giving the answer itself: " + question
                }
            ]
        }

        response = requests.post(self.__url, headers=self.__headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            print("Response from OpenAI:", response.json())
            print('\n')
            print(response.json()['choices'][0]['message']['content'])
        else:
            print("Error:", response.status_code, response.text)


    def get_feedback_from_chatgpt(self, question : str, answer : str):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant who gives feedback in detail."
                },
                {
                    "role": "user",
                    "content": "Give feedback about the answer in an interview. \nQuestion: " + question + "\nAnswer: " + answer
                }
            ]
        }

        response = requests.post(self.__url, headers=self.__headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            print("Response from OpenAI:", response.json())
            print('\n')
            print(response.json()['choices'][0]['message']['content'])
        else:
            print("Error:", response.status_code, response.text)