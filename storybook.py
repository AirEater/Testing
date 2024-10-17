from openai import OpenAI
# from IPython.display import Image
import os
import streamlit as st #important

# my_secret = os.environ['OPENAI_API_KEY']
my_secret = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=my_secret)

# Story
def story_generate(prompt):
  system_prompt = """
  You are a world-renowned author of young adult fiction stories.
  Given a concept, generate a story relevant to the themes of the concept with a twist ending.
  """

  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": prompt},
      ],
      temperature = 1.3,
      max_tokens = 15000
  )

  return response.choices[0].message.content

def art_generate(prompt):
  response = client.images.generate(
    model = 'dall-e-3',
    prompt=prompt,
    n=1,
    size="1024x1024"
  )
  image_url = response.data[0].url
  return image_url

# Cover prompt design
system_prompt = """
You will be given a story. Generate a prompt for a cover art that is suitable for the story.
The prompt is for dall-e-3.
"""

def design_gen(prompt):
  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {"role":'system', 'content':system_prompt},
          {"role":'user', 'content':prompt}
      ],
      temperature = 1.3,
      max_tokens = 5000
  )
  return response.choices[0].message.content

prompts = st.text_input("What story you are going to generate?: ")

if st.button("Generate"):
  story = story_generate(prompts)
  print(story)
  # The three major forces had a dispute and started a war

  # Generate Cover without well prompt
  art = art_generate(story)
  st.image(art)
  print(story)

  # Generate Cover with well prompt
  cover_prompt = design_gen(story)
  art = art_generate(cover_prompt)

  st.caption(cover_prompt)
  st.divider()
  st.write(story)
  st.divider()
  st.image(art)