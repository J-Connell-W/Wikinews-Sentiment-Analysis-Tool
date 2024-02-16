<script lang="ts">
  import "@picocss/pico";

  let successStatus = " ";

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault(); // Prevent the normal submission of the form
    const form = event.target as HTMLFormElement;
    const data = new FormData(form);
    const value = Object.fromEntries(data.entries());

    // Construct the object to match the `Story` model
    const story = {
      id: data.get("id"), // Assuming you have a field for the 'id' in your form
      original_language: data.get("original_language"),
      translation_language: data.get("translation_language"),
    };

    try {
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
        console.log("success", result);
      }
      if (!response.ok) {
        successStatus = "no";
        throw new Error(`Error: ${response.status}`);
      }
    } catch (error) {
      console.error("There was an error submitting the form", error);
    }
  }
</script>

<h1>Welcome to the WikiNews Story Tool</h1>
<form on:submit={handleSubmit}>
  <fieldset>
    <label>
      Story Url
      <input
        name="id"
        placeholder="Enter the URL of the story"
        autocomplete="given-name"
      />
    </label>
    <select
      name="original_language"
      aria-label="Select the story's original language..."
      required
    >
      <option selected disabled value="">
        Select the story's original language...
      </option>
      <option>English</option>
      <option>Spanish</option>
    </select>
    <select
      name="translation_language"
      aria-label="Select the language you want to translate to..."
      required
    >
      <option selected disabled value="">
        Select the language you want to translate to...
      </option>
      <option>English</option>
      <option>Spanish</option>
    </select>
  </fieldset>

  <input type="submit" value="Submit" />
</form>

{#if successStatus == "yes"}
  <p>Story submitted successfully!</p>
{/if}

{#if successStatus == "no"}
  <p>There was an error submitting the form</p>
{/if}
