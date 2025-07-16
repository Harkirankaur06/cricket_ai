async function predict() {
  const batter = document.getElementById("batter").value;
  const bowler = document.getElementById("bowler").value;
  const venue = document.getElementById("venue").value;
  const batting_team = document.getElementById("batting_team").value;
  const bowling_team = document.getElementById("bowling_team").value;
  const over = parseFloat(document.getElementById("over").value);
  const ball = parseFloat(document.getElementById("ball").value);

  // Create a combined float overs value (e.g., 5.3 becomes 5.3 overs)
  const overs = over + ball / 10;

  const inputData = {
    batting_team: batting_team,
    bowling_team: bowling_team,
    venue: venue,
    batsman: batter,
    bowler: bowler,
    runs: 0,
    wickets: 1,
    overs: overs
  };

  try {
    const [runsResponse, wicketResponse] = await Promise.all([
      fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputData)
      }).then(res => res.json()),
      fetch("/predict_wicket", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputData)
      }).then(res => res.json())
    ]);

    let output = "";

    if (runsResponse.predicted_runs !== undefined) {
      output += `Predicted Runs: ${runsResponse.predicted_runs} `;
    } else {
      output += `Runs Prediction Error: ${runsResponse.error || "Unknown"}`;
    }

    if (wicketResponse.wicket !== undefined) {
      output += `<br>Wicket Prediction: ${wicketResponse.wicket ? "❌ Wicket!" : "✅ Not Out"}`;
    } else {
      output += `<br>Wicket Prediction Error: ${wicketResponse.error || "Unknown"}`;
    }

    document.getElementById("output").innerHTML = output;
  } catch (err) {
    document.getElementById("output").innerText = "⚠️ Error: " + err.message;
  }
}
