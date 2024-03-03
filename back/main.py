from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Story, NoTranslationStory
from typing import Union
import central as c
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "I like Bananas"}


# Set up CORS middleware options
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


stories = []


# Get all stories
@app.get("/stories")
async def get_stories():
    return stories


# Get a story
@app.get("/story/{story_url}")
async def get_story(story_url: str):
    for story in stories:
        if story.id == story_url:
            return story
    return {"message": "Story not found!"}


@app.post("/story")
async def create_story(story: Union[Story, NoTranslationStory]):
    stories.append(story)
    send_to_front = c.master_function(story)
    if type(send_to_front) == dict:
        json_data = json.dumps(send_to_front)

        # Define the path to the frontend Data folder
        file_path = "../front/my-app/src/Data/dummy_data_move_to_static_and_format.json"

        # Write the JSON data to the file
        with open(file_path, "w") as file:
            file.write(json_data)

        return json_data
    else:
        return {"message": "Story object has been created!"}


# Delete a story
@app.delete("/story/{story_url}")
async def delete_story(story_id: str):
    for story in stories:
        if story.id == story_id:
            stories.remove(story)
            return {"message": "Story has been deleted!"}
    return {"message": "Story not found!"}
