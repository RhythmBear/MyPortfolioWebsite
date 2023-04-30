// api.js

// Get a reference to the <p> tag element
const purecounterElement = document.querySelector('.purecounter');

// Make an HTTP request to the API endpoint
fetch('https://github-loc-api.onrender.com/Rhythmbear')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Check if the API response contains a valid value for the <p> tag
    if (data['response'] === 200) {
      // If the API response contains a valid value for the <p> tag, update the inner text
      purecounterElement.setAttribute('data-purecounter-end', data['data']['Total lines']);
    } else {
      // If the API response does not contain a valid value for the <p> tag, set a default value
      purecounterElement.setAttribute('data-purecounter-end', '899223');
    }
  })
  .catch(error => {
    // Handle any errors that occurred during the API call
    console.error('Error:', error);
  });
