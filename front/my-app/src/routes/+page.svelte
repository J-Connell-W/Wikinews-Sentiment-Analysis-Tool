<script lang="ts">
  import "@picocss/pico";
  import { writable } from "svelte/store";
  import { slide } from "svelte/transition";
  import { onMount } from "svelte";
  import { Status, LanguageOptions, DisplayGroup } from "../Data/Enums";
  let successStatus = " ";
  let fullOriginalTextSplit = writable<string[]>([]);
  let translationText = writable<string>("");
  let summarizationText = writable<string>("");
  let summarizationTranslationText = writable<string>("");
  let sentimentAnalysisLabel = writable<string>("");
  let sentimentAnalysisScore = writable<string>("");

  // Variables for the SVGs
  // Dependency Parsing SVG Vars
  let displacyDepSvg = writable<string | null>("");
  let activeIndexDep = writable<number>(-1);
  let individualDepSVGs = writable<string[]>([]);
  // Named Entity Recognition SVG Vars
  let Ner = writable<string>("");
  //custom model error
  let customModelError = writable<string>("");

  // variables for the dropdown selections
  let originalLanguage = writable("English");
  let translationLanguage = writable("Spanish");

  // Enum for state of the application

  let currentStatus = writable<Status>(Status.INITIAL);

  // Enum for the language options as an array to use in the dropdowns
  const languageOptions = Object.values(LanguageOptions);

  let isThereTranslation = writable<DisplayGroup>(DisplayGroup.NOTRANSLATION);

  let currentDisplayGroup = DisplayGroup.UNSELECTED;

  let storyToSend = {};

  // The checkboxes with their names, checked value, and info text for the info icon hover text.
  let checkboxes = [
    {
      name: "Translate",
      checked: true,
      infoText: "Would you like to translate the news article?",
    },
    {
      name: "Summarize",
      checked: true,
      infoText: "Would you like to summarize the article?",
    },
    {
      name: "Vizualize",
      checked: true,
      infoText: "Only stories originally in English.",
    },
  ];

  // Functions to handle the display state of the tabs
  function translationTab() {
    currentDisplayGroup = DisplayGroup.TRANSLATION;
  }
  function sentimentTab() {
    currentDisplayGroup = DisplayGroup.SENTIMENT;
  }
  function summarizationTab() {
    currentDisplayGroup = DisplayGroup.SUMMARIZATION;
  }
  function summarizationTranslationTab() {
    currentDisplayGroup = DisplayGroup.SUMMARIZATION_TRANSLATION;
  }
  function visualizationTab() {
    currentDisplayGroup = DisplayGroup.VISUALIZATION;
  }

  /**
   * Function to format the sentence with a period at the end
   * @param sentence
   * @param isLast
   */
  function formatSentence(sentence: string, isLast: boolean) {
    // Check if the sentence ends with a period
    if (!isLast && !sentence.trim().endsWith(".")) {
      return `${sentence}. `;
    }
    return `${sentence}. `;
  }

  // Reactive statement to split SVGs
  $: $displacyDepSvg, splitSVGs($displacyDepSvg, "dep");

  // Function to split SVGs
  function splitSVGs(svgString: string | null, type: "dep") {
    if (svgString === null) {
      return;
    }

    // Regular expression to match the SVG tags
    const svgPattern = /<svg[\s\S]*?<\/svg>/g;
    // Ensure we default to an empty array if no matches are found
    const matches = svgString.match(svgPattern);
    individualDepSVGs.set(matches ?? []);
  }
  function setActiveSVG(index: number, type: "dep") {
    activeIndexDep.set(index);
  }
  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault(); // Prevent the normal submission of the form
    const form = event.target as HTMLFormElement;
    const data = new FormData(form);

    // Construct the object to match the `Story` model
    const story = {
      id: data.get("id"),
      original_language: data.get("original_language"),
      translation_language: data.get("translation_language"),
      summarization: checkboxes[1].checked,
      visualization: checkboxes[2].checked,
    };
    const storyNoTanslation = {
      id: data.get("id"),
      original_language: data.get("original_language"),
      summarization: checkboxes[1].checked,
      visualization: checkboxes[2].checked,
    };

    try {
      // if the tranlsation box is checked.
      if (isThereTranslation && checkboxes[0].checked) {
        storyToSend = story;
      } else {
        storyToSend = storyNoTanslation;
      }
      currentStatus.set(Status.LOADING);
      const response = await fetch("http://localhost:8000/story/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(storyToSend),
      });
      if (response.ok) {
        const result = await response.json();
        successStatus = "yes";
        const fromJsonToObject = JSON.parse(result);
        if (fromJsonToObject.story_content_split_sentences !== undefined) {
          fromJsonToObject.story_content_split_sentences.forEach(
            (element: any) => {
              element = element + ". ";
            }
          );

          fullOriginalTextSplit.set(
            (
              fromJsonToObject.story_content_split_sentences as (
                | string
                | null
                | undefined
              )[]
            ).filter(
              (sentence): sentence is string =>
                typeof sentence === "string" && sentence.trim() !== ""
            )
          );
        }

        translationText.set(fromJsonToObject.translation);
        summarizationText.set(fromJsonToObject.summarization);
        summarizationTranslationText.set(
          fromJsonToObject.summarizationTranslated
        );
        sentimentAnalysisLabel.set(fromJsonToObject.sentiment_label);
        sentimentAnalysisScore.set(fromJsonToObject.sentiment_score);
        displacyDepSvg.set(fromJsonToObject.html_get_dep);
        Ner.set(fromJsonToObject.html_get_ner);
        customModelError.set(fromJsonToObject.custom_model_error);

        if (fromJsonToObject.translation === undefined) {
          isThereTranslation.set(DisplayGroup.NOTRANSLATION);
        } else if (fromJsonToObject.translation !== undefined) {
          isThereTranslation.set(DisplayGroup.TRANSLATION);
        } else {
          isThereTranslation.set(DisplayGroup.NOTRANSLATION);
        }
        currentStatus.set(Status.SUCCESS);
      } else {
        currentStatus.set(Status.ERROR);
        throw new Error(`Error: ${response.status}`);
      }
    } catch (error) {
      console.error("There was an error submitting the form", error);
      currentStatus.set(Status.ERROR);
    }
  }

  /**
   * Check the URL to determine the source language
   * @param event
   */
  function checkUrlSourceLanguage(event: Event) {
    const target = event.target as HTMLInputElement;
    const url = target.value;
    const urlLanguage = url.split(".")[0].split("//")[1];
    if (urlLanguage === "es") {
      originalLanguage.set("Spanish");
      translationLanguage.set("English");
    } else if (urlLanguage === "en") {
      originalLanguage.set("English");
      translationLanguage.set("Spanish");
    } else if (urlLanguage === "de") {
      originalLanguage.set("German");
      translationLanguage.set("English");
    } else {
      originalLanguage.set("English");
      translationLanguage.set("Spanish");
    }
  }
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

<div class="main-background-color" id="the-body">
  <div class="standard-margin" id="body-contents">
    <header>
      <h1 class="title title-color">Welcome to the WikiNews Story Tool</h1>
    </header>
    <div class="standard-margin" id="about-section">
      <h2 class="main-accent-color">About</h2>
      <p class="main-accent-color">
        Welcome to our site! Here, you can transform any article by simply
        entering its URL. You may choose to translate it into your preferred
        language options of: English, Spanish, and German. Our tool includes
        more than translation; it delves into sentiment analysis, offering
        insight into the article's emotional tone. For a concise overview, our
        summarization feature distills the core information. Plus, experience a
        unique perspective with displaCy, visualizing text structure through
        dependency and sentence parsing. Join us in experiencing news in a whole
        new way.
      </p>
    </div>
    {#if $currentStatus !== Status.LOADING}
      <div id="main-body">
        <div id="content-wrapper">
          <form
            id="main-form"
            class="standard-margin-bottom"
            on:submit={handleSubmit}
          >
            <fieldset>
              <!-- Input and labels go here -->
              <label class="main-accent-color">
                Story Url<em
                  class="info-icon"
                  data-tooltip="Example: https://es.wikinews.org/wiki/story"
                  >?</em
                >
                <br />
                <input
                  name="id"
                  class="form-input-colors"
                  id="url-input"
                  placeholder="Enter the URL of the story"
                  required
                  on:change={checkUrlSourceLanguage}
                />
              </label>
              <label for="dropdown1" class="main-accent-color"
                >Source Language<em
                  class="info-icon"
                  data-tooltip="Select the original language of the news article."
                  >?</em
                ></label
              >
              <select
                bind:value={$originalLanguage}
                id="dropdown1"
                class="form-input-colors"
                name="original_language"
                on:change={handleDropdownChange}
              >
                {#each languageOptions as option}
                  <option value={option}>{option}</option>
                {/each}
              </select>
              <div style="font-size:1.1em" class="main-accent-color">
                Choose what you would like the tool to do with the news story.
              </div>
              <div
                style="font-size:.9em; padding-top:10px; padding-bottom:10px;"
                class="main-accent-color"
              >
                Visualization is only available for stories that originate in
                English. No button will show up for visualization even if it is
                selected given a story of a different language.
              </div>
              <div
                style="font-size:.9em; padding-top:10px; padding-bottom:10px;"
                class="main-accent-color"
              >
                If none are chosen, then by default only Sentiment Analysis will
                happen.
              </div>
              {#each checkboxes as checkbox, index (checkbox.name)}
                <label class="main-accent-color">
                  <input
                    class="checkbox-translation-background-color"
                    type="checkbox"
                    name="translation_checkbox"
                    bind:checked={checkboxes[index].checked}
                  />
                  {checkbox.name}
                  <em class="info-icon" data-tooltip={checkbox.infoText}>?</em>
                </label>
              {/each}
              {#if checkboxes[0].checked}
                <div id="translation-language-container" transition:slide>
                  <label for="dropdown2" class="main-accent-color"
                    >Translation Language <em
                      class="info-icon main-accent-color"
                      data-tooltip="Select the language to translate the article to."
                      >?</em
                    ></label
                  >
                  <select
                    bind:value={$translationLanguage}
                    id="dropdown2"
                    class="form-input-colors"
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
            <input
              class="bttn bttn main-background-color"
              id="submit-btn"
              type="submit"
              value="Submit"
            />
          </form>
        </div>
      </div>
    {/if}

    {#if $currentStatus === Status.LOADING || $currentStatus === Status.ERROR}
      <div class="loading-div">
        {#if $currentStatus === Status.LOADING}
          <div class="loading-text spinner-color">
            Running The Story Through AI Please Wait...
          </div>
          <div class="loading-icon" />
        {:else}
          <div class="loading-text main-accent-color">
            There Was An Error Running The Story
          </div>
        {/if}
      </div>
    {:else if $currentStatus === Status.SUCCESS}
      <div id="output-container">
        {#if currentDisplayGroup === DisplayGroup.UNSELECTED}
          <div class="output-sections" id="unselected-section">
            <h2 class="main-accent-color">
              Please select a tab to view the output
            </h2>
          </div>
        {/if}
        {#if $isThereTranslation === DisplayGroup.NOTRANSLATION}
          <div class="button-grouping" role="group">
            {#if $summarizationText}
              <button class="bttn" on:click={summarizationTab}
                >Summarization</button
              >
              <button class="bttn" on:click={sentimentTab}>Sentiment</button>
            {/if}
            {#if $displacyDepSvg}
              <button class="bttn" on:click={visualizationTab}
                >Visualization</button
              >
            {/if}
          </div>
        {:else if $isThereTranslation === DisplayGroup.TRANSLATION}
          <div class="button-grouping" role="group">
            {#if $translationText}
              <button class="bttn" on:click={translationTab}>Translation</button
              >
            {/if}
            {#if $summarizationTranslationText && summarizationTranslationTab}
              <button class="bttn" on:click={summarizationTranslationTab}
                >Summarization</button
              >
            {/if}
            <button class="bttn" on:click={sentimentTab}>Sentiment</button>
            {#if $displacyDepSvg}
              <button class="bttn" on:click={visualizationTab}
                >Visualization</button
              >
            {/if}
          </div>
        {/if}

        {#if currentDisplayGroup === DisplayGroup.TRANSLATION}
          <div class="output-sections" id="translation-section">
            <div id="original-text">
              <h3 class="main-accent-color">Original Text</h3>
              {#each $fullOriginalTextSplit as sentence, index}
                <span class="originalTextSpan main-accent-color"
                  >{formatSentence(
                    sentence,
                    index === $fullOriginalTextSplit.length - 1
                  )}</span
                >
              {/each}
            </div>
            <div id="translation-text">
              <h3 class="main-accent-color">Translation</h3>
              <p class="main-accent-color">{$translationText}</p>
            </div>
          </div>
        {:else if currentDisplayGroup === DisplayGroup.SUMMARIZATION}
          <div class="standard-margin summary-alone">
            <h3 class="main-accent-color">Summary</h3>
            <p class="main-accent-color">{$summarizationText}</p>
          </div>
        {:else if currentDisplayGroup === DisplayGroup.SUMMARIZATION_TRANSLATION}
          <div class="output-sections" id="translation-section">
            <div id="translation-text">
              <h3 class="main-accent-color">Translated Summary</h3>
              <p class="main-accent-color">{$summarizationTranslationText}</p>
            </div>
            <div id="original-text">
              <h3 class="main-accent-color">Original Text Summary</h3>
              <p class="main-accent-color">{$summarizationText}</p>
            </div>
          </div>
        {:else if currentDisplayGroup === DisplayGroup.SENTIMENT}
          <div class="standard-margin" id="sentiment-section">
            <h3 class="main-accent-color">Sentiment Analysis</h3>
            <p class="main-accent-color">
              Sentiment: {$sentimentAnalysisLabel}
            </p>
            <p class="main-accent-color">
              Label: {$sentimentAnalysisScore}
            </p>
          </div>
        {:else if currentDisplayGroup === DisplayGroup.VISUALIZATION}
          <div class="output-sections" id="visualization-section">
            <div id="displacy-section">
              <h2 class="main-accent-color">DisplaCy</h2>
              <p class="main-accent-color">
                DisplaCy is a visualizer for rich text annotations. It is
                designed to provide a visual impression of the syntactic
                structure of a text. The visualizer can be used to display named
                entities, part-of-speech tags, and syntactic dependencies. It is
                a great tool for understanding the structure of a news article.
              </p>
              <p class="main-accent-color">
                This tool allows you to click on a sentence to view its
                dependency parsing, which illustrates the relationships between
                words based on the source language. We opted for the source
                language in the visualization section to maintain accuracy, as
                translations by the model may alter the original meaning.
              </p>
            </div>
            <div id="displacy-original-text">
              <h3 class="main-accent-color">
                Click on a Sentence or press Enter when focused.
              </h3>
              {#each $fullOriginalTextSplit as sentence, index}
                <div class="sentence-container">
                  <button
                    class="bttn dep-bttn"
                    on:click={() => setActiveSVG(index, "dep")}
                    tabindex="0"
                  >
                    {formatSentence(
                      sentence,
                      index === $fullOriginalTextSplit.length - 1
                    )}
                  </button>
                  <!-- Render SVG directly below the button if it is the active index -->
                  {#if $activeIndexDep === index}
                    <div class="svg-container">
                      {@html $individualDepSVGs[$activeIndexDep]}
                    </div>
                  {/if}
                </div>
              {/each}
              <div class="ner-container">
                <h3>Named Entity Recognition</h3>
                {@html $Ner}
              </div>
            </div>
          </div>
        {/if}
      </div>
    {/if}
  </div>
  <footer>Made by Joel Connell and Thomas Mendenhall</footer>
</div>

<style>
  header {
    text-align: center;
  }
  .title {
    text-shadow: 1.5px 1px 0px #6b4e1f;
    color: #f5a628;
  }
  #content-wrapper {
    margin-top: 50px;
  }
  #the-body {
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
  #body-contents {
    flex-grow: 1;
  }

  label {
    font-weight: bold;
  }
  .checkbox-translation-background-color {
    background-color: #f5a628;
  }
  .main-background-color {
    background-color: rgb(51, 52, 57);
  }
  .main-accent-color {
    color: #f5a628;
  }

  .info-icon {
    padding-left: 10px;
    padding-right: 10px;
    width: 10px;
    height: 10px;
    margin-left: 15px;
    border-radius: 50%;
    background-color: #000000;
    border: solid 3px #f5a628;
    box-shadow: inset 0px 0px 2px 0px #6b4e1f;
  }
  #main-form {
    color: #d5ddc5;
  }
  #url-input {
    margin: 30px;
    background-color: #d3d3d3;
    color: #0c0c0c;
    width: 70%;
  }
  #translation-language-container {
    margin-top: 25px;
  }
  select {
    margin: 30px;
    color: #0c0c0c;
    width: 30%;
  }
  .form-input-colors {
    background-color: #d3d3d3;
    color: #0c0c0c;
  }
  .bttn {
    background-color: #7f1f0a;
    border: 2px solid #442f38;
    color: #fffcff;
    width: 33%;
    margin: auto;
  }
  .bttn:hover {
    background-color: #53180b;
    border: 2px solid #361010;
    color: #fffcff;
  }
  .bttn:focus {
    background-color: #53180b;
    border: 2px solid #361010;
    color: #fffcff;
  }

  .button-grouping {
    width: 100%;
    padding: 50px;
    --pico-group-box-shadow: none;
  }
  .button-grouping button {
    --pico-group-box-shadow: none;
    background-color: #bc5750;
    color: black;
  }
  .button-grouping:focus button {
    --pico-group-box-shadow: none;
  }

  .loading-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: 50px;
    margin-right: 50px;
    font-size: 3em;
    justify-content: center;
  }
  .loading-icon {
    border: 25px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 20px solid #f5a628;
    margin-top: 50px;
    margin-left: 20px;
    width: 200px;
    height: 200px;
    -webkit-animation: spin 2s linear infinite; /* Safari */
    animation: spin 2s linear infinite;
  }

  /* Safari */
  @-webkit-keyframes spin {
    0% {
      -webkit-transform: rotate(0deg);
    }
    100% {
      -webkit-transform: rotate(360deg);
    }
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  .standard-margin {
    margin-left: 50px;
    margin-right: 50px;
    margin-top: 50px;
  }
  .standard-margin-bottom {
    margin-left: 50px;
    margin-right: 50px;
    margin-bottom: 50px;
  }
  .spinner-color {
    color: #f5a628;
  }
  .ner-container {
    padding: 15px;
    margin-top: 30px;
    border: #f5a628 solid 2px;
  }
  .ner-container h3 {
    color: #f5a628;
  }
  .svg-container {
    margin-top: 0.5em;
    width: 100%;
    overflow: auto;
    display: flex;
    flex-direction: column;
  }
  #translation-section {
    margin-left: 50px;
    margin-right: 50px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 50px;
  }
  .output-sections {
    margin-left: 50px;
    margin-right: 50px;
    margin-top: 50px;
  }

  #translation-text {
    width: 45%;
    padding-top: 25px;
    padding-left: 30px;
    padding-right: 30px;
    border: #f5a628 solid 2px;
  }
  #original-text {
    width: 45%;
    padding-top: 25px;
    padding-left: 30px;
    padding-right: 30px;
    padding-bottom: 25px;
    border: #f5a628 solid 2px;
  }
  .summary-alone {
    margin: auto;
    padding-top: 25px;
    padding-left: 30px;
    padding-right: 30px;
    padding-bottom: 25px;
    margin-bottom: 50px;
    border: #f5a628 solid 2px;
  }

  #sentiment-section {
    width: fit-content;
    margin: auto;
    padding-top: 25px;
    padding-left: 30px;
    padding-right: 30px;
    padding-bottom: 25px;
    margin-bottom: 50px;
    border: #f5a628 solid 2px;
  }
  #displacy-original-text {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.5em;
  }
  .dep-bttn {
    width: 100%;
  }
  .originalTextSpan:focus {
    cursor: pointer;
    display: inline-block;
    outline: none;
    border: 1px solid #aaa; /* Custom focus style */
    border-radius: 4px;
    padding: 2px;
    background-color: #3d5f2f8b;
  }
  footer {
    margin-top: 15px;
    text-align: center;
    color: #2b2b2b;
    font-size: 1.1em;
    background-color: #f5a628;
    width: 100%;
    height: 50px;
  }
</style>
