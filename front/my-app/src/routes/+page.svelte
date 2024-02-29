<script lang="ts">
  import "@picocss/pico";
  import { writable } from "svelte/store";
  import { slide } from "svelte/transition";

  let successStatus = " ";

  // svgForDisplacy
  let fullOriginalTextSplit = writable<string[]>([]);
  let svgDisplacy = writable<string>("");
  let summarizationText = writable("");
  let sentimentAnalysisLabel = writable("");
  let sentimentAnalysisScore = writable("");
  let translationText = writable("");
  let activeIndex: number | null = null;
  let activeIndexSVG = writable<number>(-1);
  let individualSVGs = writable<string[]>([]);
  enum status {
    INITIAL = "Initial",
    LOADING = "Loading",
    SUCCESS = "Success",
    ERROR = "Error",
  }
  let currentStatus = status.INITIAL;

  enum displayGroup {
    TRANASLATION = "Translation",
    SENTIMENT = "Sentiment",
    SUMMARIZATION = "Summarization",
    VISUALIZATION = "Visualization",
  }
  let currentDisplayGroup = displayGroup.TRANASLATION;

  function translationTab() {
    currentDisplayGroup = displayGroup.TRANASLATION;
  }
  function sentimentTab() {
    currentDisplayGroup = displayGroup.SENTIMENT;
  }
  function summarizationTab() {
    currentDisplayGroup = displayGroup.SUMMARIZATION;
  }
  function visualizationTab() {
    currentDisplayGroup = displayGroup.VISUALIZATION;
  }

  function formatSentence(sentence: string, isLast: boolean) {
    // Check if the sentence ends with a period
    if (!isLast && !sentence.trim().endsWith(".")) {
      return `${sentence}. `;
    }
    return `${sentence}. `;
  }
  // Function to handle sentence click
  function handleSentenceSelect(index: number) {
    activeIndex = index;
    // Logic to display the corresponding SVG goes here
  }
  // Reactive statement to split SVGs
  $: $svgDisplacy, splitSVGs($svgDisplacy);

  // Function to split SVGs
  function splitSVGs(svgString: string) {
    const svgPattern = /<svg[\s\S]*?<\/svg>/g;
    // Ensure we default to an empty array if no matches are found
    const matches = svgString.match(svgPattern);
    individualSVGs.set(matches ?? []);
  }
  function setActiveSVG(index: number) {
    activeIndexSVG.set(index);
  }
  // Reactive variable to track the active SVG index

  // Function to set the active SVG index
  function setActiveIndexSVG(index: number) {
    activeIndexSVG.set(index);
  }

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
      currentStatus = status.LOADING;
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
        svgDisplacy.set(fromJsonToObject.html_get_dep);
        summarizationText.set(fromJsonToObject.summarization);
        sentimentAnalysisLabel.set(fromJsonToObject.sentiment_label);
        sentimentAnalysisScore.set(fromJsonToObject.sentiment_score);
        translationText.set(fromJsonToObject.translation);
        console.log($fullOriginalTextSplit);
        console.log($summarizationText);
        console.log($translationText);
        console.log(fromJsonToObject);
        console.log($svgDisplacy);
        currentStatus = status.SUCCESS;
      }
      if (!response.ok) {
        currentStatus = status.ERROR;
        throw new Error(`Error: ${response.status}`);
      }
    } catch (error) {
      console.error("There was an error submitting the form", error);
      currentStatus = status.ERROR;
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

<div id="the-body">
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
  {#if currentStatus !== status.LOADING}
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
              <br />
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
                data-tooltip="Would you like to translate the news article?"
                >?</em
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
      </div>
    </div>
  {/if}

  {#if currentStatus === status.LOADING || currentStatus === status.ERROR}
    <div class="loading-div">
      {#if currentStatus === status.LOADING}
        <div class="loading-text">
          Running The Story Through AI Please Wait...
        </div>
        <div class="loading-icon" />
      {:else}
        <div class="loading-text">There Was An Error Running The Story</div>
      {/if}
    </div>
  {:else if currentStatus === status.SUCCESS}
    <div id="button-grouping" role="group">
      <button on:click={translationTab}>Translation</button>
      <button on:click={summarizationTab}>Summarization</button>
      <button on:click={sentimentTab}>Sentiment</button>
      <button on:click={visualizationTab}>Visualization</button>
    </div>
    {#if currentDisplayGroup === displayGroup.TRANASLATION}
      <div class="output-sections" id="translation-section">
        <div id="translation-text">
          <h3 class="red">Translation</h3>
          <p>{$translationText}</p>
        </div>
        <div id="original-text">
          <h3 class="red">Original Text</h3>
          {#each $fullOriginalTextSplit as sentence, index}
            <span class="originalTextSpan"
              >{formatSentence(
                sentence,
                index === $fullOriginalTextSplit.length - 1
              )}</span
            >
          {/each}
        </div>
      </div>
    {:else if currentDisplayGroup === displayGroup.SUMMARIZATION}
      <div class="output-sections" id="summarization-section">
        <h3 class="red">Summarization</h3>
        <p>{$summarizationText}</p>
      </div>
    {:else if currentDisplayGroup === displayGroup.SENTIMENT}
      <div class="output-sections" id="sentiment-section">
        <h3 class="red">Sentiment Analysis</h3>
        <p>
          Sentiment: {$sentimentAnalysisLabel}
        </p>
        <p>
          Label: {$sentimentAnalysisScore}
        </p>
      </div>
    {:else if currentDisplayGroup === displayGroup.VISUALIZATION}
      <div class="output-sections" id="visualization-section">
        <div id="displacy-section">
          <h2>DisplaCy</h2>
          <p>
            DisplaCy is a visualizer for rich text annotations. It is designed
            to provide a visual impression of the syntactic structure of a text.
            The visualizer can be used to display named entities, part-of-speech
            tags, and syntactic dependencies. It is a great tool for
            understanding the structure of a news article.
          </p>
          <p>
            For this tool you can click on a sentence to see its dependency
            parsing. Dependency parsing shows how words are related to others.
          </p>
        </div>
        <div class="output-sections" id="displacy-original-text">
          <h3 class="red">Click on a Sentence or press Enter when focused.</h3>
          {#each $fullOriginalTextSplit as sentence, index}
            <div class="sentence-container">
              <button
                class="dep-buttons"
                on:click={() => setActiveSVG(index)}
                tabindex="0"
              >
                {formatSentence(
                  sentence,
                  index === $fullOriginalTextSplit.length - 1
                )}
              </button>
              <!-- Render SVG directly below the button if it is the active index -->
              {#if $activeIndexSVG === index}
                <div class="svg-container">
                  {@html $individualSVGs[$activeIndexSVG]}
                </div>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}
  {/if}
  <footer>Made by Joel Connell and Thomas Mendenhall</footer>
</div>

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
  #the-body {
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
  .originalTextSpan {
    color: #3d0814;
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
  #main-form {
    width: 80vw;
    margin: auto;
    color: #d5ddc5;
  }
  #url-input {
    margin: 30px;
    background-color: #cbe2c2;
    color: #0c0c0c;
    width: 70%;
  }
  #translation-language-container {
    margin-top: 25px;
  }
  select {
    margin: 30px;
    background-color: #cbe2c2;
    color: #0c0c0c;
    width: 30%;
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
  #button-grouping {
    width: 80vw;
    margin: auto;
    margin-top: 50px;
  }
  #button-grouping button {
    border: 2px solid #000000;
    background-color: #3d0814;
  }
  #button-grouping button:hover {
    background-color: #442f38;
    color: #f194b4;
    border-color: #361010;
  }
  #button-grouping button:focus {
    background-color: #442f38;
    color: #f194b4;
    border-color: #361010;
  }
  #displacy-section {
    margin: 50px;
    color: #3d0814;
  }
  .loading-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-left: 50px;
    margin-right: 50px;
    font-size: 3em;
    justify-content: center;
    flex-grow: 1;
  }
  .loading-icon {
    border: 25px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 20px solid #2d729f;
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
  .loading-text {
    color: #3d0814;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
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

  #summarization-section {
    margin-left: 50px;
    margin-right: 50px;
    margin-top: 50px;
  }
  #translation-text {
    width: 45%;
    padding-left: 20px;
    padding-right: 20px;
    border: #361010 solid 2px;
  }
  #original-text {
    width: 45%;
    padding-left: 20px;
    padding-right: 20px;
    border: #361010 solid 2px;
  }
  #displacy-original-text {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
  }
  .dep-buttons {
    background-color: #3d0814;
    color: #91c499;
    border: 2px solid #000000;
    border-radius: 5px;
    text-align: left;
  }
  .dep-buttons:hover {
    background-color: #442f38;
    color: #f194b4;
    border-color: #361010;
  }
  .dep-buttons:focus {
    background-color: #442f38;
    color: #f194b4;
    border-color: #361010;
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
    color: #91c499;
    font-size: 1.1em;
    background-color: #234f1e;
    width: 100%;
    height: 50px;
  }
</style>
