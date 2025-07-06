console.log("Analytics script loaded");

const TRACK_URL = "http://35.200.226.132:5002/track";

function sendEvent(eventType) {
  const payload = {
    event_type: eventType,
    page_url: window.location.pathname
  };

  console.log("Sending event:", payload);

  fetch(TRACK_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
  .then(res => {
    console.log(`Response status: ${res.status}`);
    return res.text();
  })
  .then(body => {
    console.log("Server said:", body);
  })
  .catch(err => {
    console.error("Error sending event:", err);
  });
}

window.addEventListener("load", () => sendEvent("page_view"));

let scrollTracked = false;
window.addEventListener("scroll", () => {
  if (!scrollTracked) {
    sendEvent("scroll");
    scrollTracked = true;
  }
});

let clickTracked = false;
document.addEventListener("click", () => {
  if (!clickTracked) {
    sendEvent("click");
    clickTracked = true;
  }
});
