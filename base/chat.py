from openai import OpenAI
import json
from django.conf import settings
import os
client = OpenAI()
def get_json(user_propmt):
  system_prompt = """Ты полезный помощник, который извлекает название места (местоположения), город и категорию покупки. Ответ должен быть в формате JSON.
  Схема ответа:
  {
      "place_name": "place name",
      "city": "city",
      "category": "category"   
  }

  """
  
  sub2parent_path = os.path.join(settings.BASE_DIR, 'base', 'sub2parent.json')
  try:
    with open(sub2parent_path, 'r') as file:
        sub2parent = json.load(file)
  except FileNotFoundError:
    raise Exception("The file sub2parent.json was not found in the specified path.")
  except json.JSONDecodeError:
    raise Exception("The file sub2parent.json is not a valid JSON.")


  categories = list(sub2parent.values())

  system_prompt += "Категории:\n"
  for category in categories:
      system_prompt += f"- {category}\n"


  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_propmt},
    ]
  )

  return json.loads(response.choices[0].message.content)
