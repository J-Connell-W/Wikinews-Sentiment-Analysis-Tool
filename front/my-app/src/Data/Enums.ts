// Purpose: Contains all the enums used in the application.

// Enum for the status of the API call, used to determine the state of the API call and Initial represents the pre first api call
export enum Status {
  INITIAL = "Initial",
  LOADING = "Loading",
  SUCCESS = "Success",
  ERROR = "Error",
}

// Enum for the language options, chooses which language is used for the translation
export enum LanguageOptions{
  ENGLISH = "English",
  SPANISH = "Spanish",
  GERMAN = "German",
}

// Enum for the display group, chooses which display is shown after clicking from button group
export enum DisplayGroup {
    TRANSLATION = "Translation",
    NOTRANSLATION = "NoTranslation",
    SENTIMENT = "Sentiment",
    SUMMARIZATION_TRANSLATION = "SummarizationTranslation",
    SUMMARIZATION = "Summarization",
    VISUALIZATION = "Visualization",
    UNSELECTED = "Unselected",
  }