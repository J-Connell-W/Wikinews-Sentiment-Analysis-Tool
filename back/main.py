from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Story

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
async def create_story(story: Story):
    stories.append(story)
    print(stories)
    return {"message": "Story object has been created!"}


# Delete a story
@app.delete("/story/{story_url}")
async def delete_story(story_id: str):
    for story in stories:
        if story.id == story_id:
            stories.remove(story)
            return {"message": "Story has been deleted!"}
    return {"message": "Story not found!"}
