# WikiNews Sentiment Analysis, Translation, Summarization Tool

## Introduction

This project is a web application that allows users to input a news article in English, German or Spanish and then translate it to one of the remaining two languages. The user can also analyze the sentiment of the article and summarize it. The project is built using HuggingFace's transformers library and FastAPI for the backend. The frontend is built using Svelte, TypeScript, and PicoCSS. This project was built by Joel connell and Thomas Mendenhall.

## Installation

We decided not to deploy this project to the web so you may clone the repository and follow these steps to run it locally. Maybe in the future we will deploy it to the web.

### Steps

These are the steps to run the project locally for VSCode. You can use any text editor or IDE you like but the steps may be different.

1. Clone the repository
2. Open the powershell terminal in VSCode and navigate to the back folder with `cd back`
3. Create a new venv and activate it
4. Run `pip install -r requirements.txt`
5. Run `uvicorn main:app --reload` to start the backend
6. **Without closing your other terminal open a new terminal** and navigate from the root by `cd front/my-app` to the folder then to my-app folder and run `npm install`
7. Run `npm run dev` to start the frontend
8. Open your browser and navigate to the address that your terminal gives you it should look like `http://localhost:5173/`

### How to use the site

- Once you have the site open you can paste a news article into the text area
- You can then select the language of the article from the dropdown
- You can then select the language you want to translate the article to from the second dropdown
- You may use the checkboxes to determine which steps you want to take with the article less options will make the process faster as it has to run through less models.

### Additional Considerations

The first running of the site may be slow as the models have to be downloaded. The models are large and may take a few minutes to download. Once the models are downloaded the site should run faster on subsequent uses. The site may also be slow if you are using a slow internet connection or a slow computer.

Also, the site may not work if you are using a VPN or are behind a firewall that blocks the models from being downloaded.

The front-end sends the article to localhost:8000/story so you will need to make sure the backend is set up for localhost:8000. If you are using a different port you will need to change the fetch request in the front-end to the correct port.

## Methodology

We will be using the following tools and libraries for this project:

- [HuggingFace](https://huggingface.co/)
- [Transformers](https://huggingface.co/transformers/)
- [Torch](https://pytorch.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Svelte](https://svelte.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Spacy](https://spacy.io/)
- [PicoCSS](https://picocss.com/)

### Models

#### Translation Models

- [Helsinki-NLP/opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-de-en)
- [Helsinki-NLP/opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-en-de)
- [Helsinki-NLP/opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-es-en)
- [Helsinki-NLP/opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-en-es)
- [Helsinki-NLP/opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-de-es)
- [Helsinki-NLP/opus-mt-de-en](https://huggingface.co/Helsinki-NLP/opus-mt-es-de)

#### Sentiment Analysis Model

- [lxyuan/distilbert-base-multilingual-cased-sentiments-student](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student)

#### Summarization Model

- [sshleifer/distilbart-cnn-12-6](https://huggingface.co/sshleifer/distilbart-cnn-12-6)

#### Visualization

The visualization step was accomplished by using Spacy's Visualization called Displacy. This shows the dependency parsing and named entity recognition of the English stories.

- [Displacy](https://spacy.io/usage/visualizers)

## License

The models used in this project are on their individual licenses you can see more about that on the model's page which should be linked above. As this is made off of HuggingFace's models we will not be providing a license for the models.
