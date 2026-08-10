async function calculate() {
    const expression =
        document.getElementById("display").value;

    const response = await fetch("/calculate/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            expression: expression
        })
    });

    const data = await response.json();

    document.getElementById("display").value =
        data.result;
}
