const form = document.querySelector('#search-form');
const results = document.querySelector('#search-results');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const input = document.querySelector('#search-input');
  const query = input.value;

  // Check if the search query is empty
  if (query.trim() === '') {
    return;
  }

  // Call the search function
  search(query)
    .then((response) => {
      // Display the search results
      displayResults(response.data);
    })
    .catch((error) => {
      // Handle any errors that occur
      console.error(error);
      results.innerHTML = 'An error occurred. Please try again later.';
    });
});

// Function to perform the search
async function search(query) {
  // Call your search API or service here
  // and return the search results
  const response = await fetch(`/search?q=${query}`);
  const data = await response.json();
  return { data };
}

// Function to display the search results
function displayResults(results) {
  // Clear the previous results
  results.innerHTML = '';

  // Create a list of search result items
  const list = document.createElement('ul');
  results.appendChild(list);

  results.forEach((result) => {
    // Create a list item for each search result
    const item = document.createElement('li');
    list.appendChild(item);

    // Add the title and description to the list item
    const title = document.createElement('h2');
    title.textContent = result.title;
    item.appendChild(title);

    const description = document.createElement('p');
    description.textContent = result.description;
    item.appendChild(description);

    // Add a link to the original web page
    const link = document.createElement('a');
    link.href = result.url;
    link.textContent = 'Read more';
    item.appendChild(link);
  });
}
