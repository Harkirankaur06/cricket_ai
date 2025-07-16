fetch("/predict_wicket", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(res => {
  const result = res.wicket ? "❌ Wicket!" : "✅ Not Out";
  document.getElementById("output").innerText = result;
})
.catch(err => {
  document.getElementById("output").innerText = "Error: " + err.message;
});
