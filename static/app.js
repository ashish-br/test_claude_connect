const form = document.getElementById("greet-form");
const message = document.getElementById("message");
const time = document.getElementById("time");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = document.getElementById("name").value;

  try {
    const response = await fetch(`/api/hello?name=${encodeURIComponent(name)}`);
    const data = await response.json();
    message.textContent = data.message;
    time.textContent = `Current time: ${data.time}`;
  } catch (error) {
    message.textContent = "Could not reach the server. Is server.py running?";
    time.textContent = "";
  }
});
