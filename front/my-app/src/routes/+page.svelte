<script lang="ts">
  import "@picocss/pico";
  import { writable } from "svelte/store";
  import { slide } from "svelte/transition";

  let successStatus = " ";

  // svgForDisplacy
  let fullOriginalTextSplit = writable("");
  let svgDisplacy = writable("");
  let summarizationText = writable("");
  let sentimentAnalysisLabel = writable("");
  let sentimentAnalysisScore = writable("");
  let translationText = writable("");

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault(); // Prevent the normal submission of the form
    const form = event.target as HTMLFormElement;
    const data = new FormData(form);

    // Construct the object to match the `Story` model
    const story = {
      id: data.get("id"), // Assuming you have a field for the 'id' in your form
      original_language: data.get("original_language"),
      translation_language: data.get("translation_language"),
    };

    try {
      console.log(story);
      const response = await fetch("http://localhost:8000/story/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(story),
      });
      if (response.ok) {
        const result = await response.json();
        successStatus = "yes";
        const fromJsonToObject = JSON.parse(result);
        console.log(fromJsonToObject.story_content);
        fromJsonToObject.story_content_split_sentences.forEach(
          (element: any) => {
            element = element + ". ";
          }
        );
        fullOriginalTextSplit.set(
          fromJsonToObject.story_content_split_sentences
        );
        svgDisplacy.set(fromJsonToObject.html_get_dep);
        summarizationText.set(fromJsonToObject.summarization);
        sentimentAnalysisLabel.set(fromJsonToObject.sentiment_label);
        sentimentAnalysisScore.set(fromJsonToObject.sentiment_score);
        translationText.set(fromJsonToObject.translation);
        console.log($fullOriginalTextSplit);
        console.log($summarizationText);
        console.log($translationText);
        console.log(fromJsonToObject);
      }
      if (!response.ok) {
        successStatus = "no";
        throw new Error(`Error: ${response.status}`);
      }
    } catch (error) {
      console.error("There was an error submitting the form", error);
    }
  }

  // Checkbox boolean
  let isChecked = false;

  // Define an array of language options
  const languageOptions = ["English", "Spanish"];

  // State variables for the dropdown selections
  let originalLanguage = writable("English");
  let translationLanguage = writable("Spanish");

  // Update the dropdowns based on selection
  function handleDropdownChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    if (target.id === "dropdown1") {
      originalLanguage.set(target.value);
      if (target.value === $translationLanguage) {
        // Find the next option that isn't the currently selected one
        const nextOption = languageOptions.find(
          (option) => option !== target.value
        );
        translationLanguage.set(nextOption!);
      }
    } else if (target.id === "dropdown2") {
      translationLanguage.set(target.value);
      if (target.value === $originalLanguage) {
        // Find the next option that isn't the currently selected one
        const nextOption = languageOptions.find(
          (option) => option !== target.value
        );
        originalLanguage.set(nextOption!);
      }
    }
  }
</script>

<body>
  <header>
    <h1>Welcome to the WikiNews Story Tool</h1>
  </header>
  <div id="about-section">
    <h2>About</h2>
    <p>
      Welcome to our site! Here, you can transform any article by simply
      entering its URL. You may choose to translate it into your preferred
      language for easier understanding. Our AI-driven platform goes beyond
      translation; it delves into sentiment analysis, offering insight into the
      article's emotional tone. For a concise overview, our summarization
      feature distills the core information. Plus, experience a unique
      perspective with displaCy, visualizing text structure through dependency
      and sentence parsing. Join us in experiencing news in a whole new way.
    </p>
  </div>
  <div id="main-body">
    <div id="content-wrapper">
      <form id="main-form" on:submit={handleSubmit}>
        <fieldset>
          <!-- Input and labels go here -->
          <label>
            Story Url<em
              class="info-icon"
              data-tooltip="Enter the Url of the WikiNews story you would like to submit."
              >?</em
            >
            <input
              name="id"
              id="url-input"
              placeholder="Enter the URL of the story"
              required
              autocomplete="given-name"
            />
          </label>
          <label>
            <input
              id="translation-checkbox"
              type="checkbox"
              name="translation_checkbox"
              bind:checked={isChecked}
            />
            Translate
            <em
              class="info-icon"
              data-tooltip="Would you like to translate the news article?">?</em
            >
          </label>

          {#if isChecked}
            <div id="translation-language-container" transition:slide>
              <label for="dropdown1"
                >Source Language<em
                  class="info-icon"
                  data-tooltip="Select the original language of the news article."
                  >?</em
                ></label
              >
              <select
                bind:value={$originalLanguage}
                id="dropdown1"
                name="original_language"
                on:change={handleDropdownChange}
              >
                {#each languageOptions as option}
                  <option value={option}>{option}</option>
                {/each}
              </select>
              <label for="dropdown2"
                >Translation Language <em
                  class="info-icon"
                  data-tooltip="Select the language to translate the article to."
                  >?</em
                ></label
              >
              <select
                bind:value={$translationLanguage}
                id="dropdown2"
                on:change={handleDropdownChange}
                name="translation_language"
              >
                {#each languageOptions as option}
                  <option value={option}>{option}</option>
                {/each}
              </select>
            </div>
          {/if}
        </fieldset>

        <input id="submit-btn" type="submit" value="Submit" />
      </form>
      {#if successStatus == "yes"}
        <p>Story submitted successfully!</p>
      {/if}

      {#if successStatus == "no"}
        <p>There was an error submitting the form</p>
      {/if}
    </div>
  </div>
  <h2>DisplaCy</h2>
  <p>
    DisplaCy is a visualizer for rich text annotations. It is designed to
    provide a visual impression of the syntactic structure of a text. The
    visualizer can be used to display named entities, part-of-speech tags, and
    syntactic dependencies. It is a great tool for understanding the structure
    of a news article.
  </p>
  <div id="displacy-section">
    {#if $fullOriginalTextSplit}
      <div>
        <h3 class="red">Original Text</h3>
        {#each $fullOriginalTextSplit as sentence}
          <span>{sentence}</span>
        {/each}
      </div>
    {/if}
    {#if $summarizationText}
      <div>
        <h3 class="red">Summarization</h3>
        <p>{$summarizationText}</p>
      </div>
    {/if}
    {#if $sentimentAnalysisLabel && $sentimentAnalysisScore}
      <div>
        <h3 class="red">Sentiment Analysis</h3>
        <p>
          Sentiment: {$sentimentAnalysisLabel}
        </p>
        <p>
          Label: {$sentimentAnalysisScore}
        </p>
      </div>
    {/if}
    {#if $translationText}
      <div>
        <h3 class="red">Translation</h3>
        <p>{$translationText}</p>
      </div>
    {/if}
    {#if $svgDisplacy}
      <div class="svg-container">
        {@html $svgDisplacy}
      </div>
    {:else}
      <div>Loading SVG...</div>
    {/if}
    <footer>Made by Joel Connell and Thomas Mendenhall</footer>
  </div></body
>

<style>
  header {
    text-align: center;
  }
  h1 {
    color: #234f1e;
    text-shadow: 0.5px 1px 0px #193716;
  }
  #content-wrapper {
    margin-top: 50px;
  }
  body {
    background-color: #91c499;
    font-size: 1.1em;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  #main-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: auto;
  }
  #about-section {
    margin: 50px;
    color: #3d0814;
  }
  h2 {
    color: #3d0814;
  }
  p {
    color: #3d0814;
  }
  span {
    color: #3d0814;
    padding: 0.25em;
  }
  label {
    color: #3d0814;
    font-weight: bold;
  }
  #translation-checkbox {
    background-color: #3d0814;
  }
  .red {
    color: #3d0814;
  }
  .info-icon {
    padding-left: 10px;
    padding-right: 10px;
    width: 10px;
    height: 10px;
    margin-left: 15px;
    border-radius: 50%;
    background-color: #c5fad1;
    border: solid 3px #234f1e;
    box-shadow: inset 0px 0px 2px 0px #234f1e;
  }
  .svg-container {
    width: 7000px;
    overflow-x: scroll;
  }
  #main-form {
    width: 66vw;
    margin: auto;
    color: #d5ddc5;
  }
  #url-input {
    background-color: #cbe2c2;
    color: #0c0c0c;
  }
  #translation-language-container {
    margin-top: 25px;
  }
  select {
    background-color: #cbe2c2;
    color: #0c0c0c;
  }
  #submit-btn {
    background-color: #3d0814;
    color: #91c499;
    width: 33%;
    margin: auto;
    border-color: #75b72e80;
  }
  #submit-btn:hover {
    background-color: #442f38;
    color: #f194b4;
    width: 33%;
    margin: auto;
    border-color: #361010;
  }
  #submit-btn:focus {
    background-color: #442f38;
    color: #f194b4;
    width: 33%;
    margin: auto;
    border-color: #361010;
  }
  footer {
    text-align: center;
    color: #91c499;
    font-size: 0.8em;
    background-color: #234f1e;
    margin-top: 15px;
    width: 100%;
  }
</style>
