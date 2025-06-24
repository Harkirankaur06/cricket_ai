function predict() {
  const data = {
    batting_team: document.getElementById("batting_team").value,
    bowling_team: document.getElementById("bowling_team").value,
    over: parseInt(document.getElementById("over").value),
    ball: parseInt(document.getElementById("ball").value),
    batter: document.getElementById("batter").value,
    bowler: document.getElementById("bowler").value,
    venue: document.getElementById("venue").value
  };

  console.log("Sending to API:", data);

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(res => {
    console.log("Response from API:", res);
    if (res.predicted_runs !== undefined) {
      document.getElementById("output").innerText = `Predicted Runs: ${res.predicted_runs}`;
    } else {
      document.getElementById("output").innerText = "⚠️ Could not get prediction.";
    }
  })
  .catch(err => {
    console.error("Fetch Error:", err);
    document.getElementById("output").innerText = "❌ Backend not responding.";
  });
}

