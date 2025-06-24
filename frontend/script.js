function predict() {
  const data = {
    batting_team: "MI",
    bowling_team: "CSK",
    over: 5,
    ball: 3,
    batter: document.getElementById("batter").value,
    bowler: document.getElementById("bowler").value,
    venue: document.getElementById("venue").value
  };

  fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json())
    .then(res => {
      document.getElementById("output").innerText = `Predicted Runs: ${res.predicted_runs}`;
    });
}
