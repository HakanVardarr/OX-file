let download_button = document.getElementsByClassName("download")[0];
let file_name = document.getElementById("file_name").innerHTML.trim();

function get_csrf_token() {
  const cookies = document.cookie.split(";");
  let csrf_token = null;
  cookies.forEach((cookie) => {
    const parts = cookie.trim().split("=");
    if (parts[0] === "csrftoken") {
      csrf_token = parts[1];
    }
  });
  return csrf_token;
}

function handle_blob(blob, file_name) {
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = file_name;
  document.body.appendChild(link);

  link.click();

  URL.revokeObjectURL(url);
  document.body.removeChild(link);
}

download_button.addEventListener("click", () => {
  const csrf_token = get_csrf_token();
  const headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,
  };
  const body = JSON.stringify({ filename: file_name });

  fetch("download", {
    method: "POST",
    headers: headers,
    body: body,
  })
    .then(async (response) => {
      if (!response.ok) {
        throw Error("Failed to initiate file download.");
      }
      return await response.blob();
    })
    .then((blob) => handle_blob(blob, file_name))
    .catch((error) => console.error("Error:", error));
});
