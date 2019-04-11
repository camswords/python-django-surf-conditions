
console.log("Welcome to the Surf Report!");

let rows = document.querySelectorAll(".more_reports tr");

rows.forEach((row) => {
    let url = row.getAttribute('data-url');

    if (url) {
        row.onclick = () => window.location.href = url;
    }
});
