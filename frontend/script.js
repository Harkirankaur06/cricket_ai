fetch("http://127.0.0.1:5000/predict_wicket", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(res => {
  const result = res.wicket ? "❌ Wicket!" : "✅ Not Out";
  document.getElementById("output").innerText = result;
});
