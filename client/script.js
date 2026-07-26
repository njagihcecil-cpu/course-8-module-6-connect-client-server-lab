const API_URL = "http://localhost:5000/events";
 
const eventList = document.querySelector("#event-list");
const form = document.querySelector("#event-form");
const titleInput = document.querySelector("#title");
const errorMsg = document.querySelector("#error-msg");
 
// Load existing events on page load
fetch(API_URL)
  .then((response) => response.json())
  .then((events) => events.forEach(renderEvent))
  .catch(() => showError("Could not load events. Is the server running?"));
 
form.addEventListener("submit", (e) => {
  e.preventDefault();
  errorMsg.textContent = "";
 
  const title = titleInput.value.trim();
 
  // Client-side validation before sending the request
  if (!title) {
    showError("Please enter a title before submitting.");
    return;
  }
 
  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data.error || "Something went wrong");
        });
      }
      return response.json();
    })
    .then((event) => {
      renderEvent(event);
      form.reset();
    })
    .catch((err) => showError(err.message));
});
 
function renderEvent(event) {
  const li = document.createElement("li");
  li.textContent = event.title;
  eventList.appendChild(li);
}
 
function showError(message) {
  errorMsg.textContent = message;
}
 