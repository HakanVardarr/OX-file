const file_input = document.getElementById("file");
const download_buttons = Array.from(
  document.getElementsByClassName("download")
);
const delete_buttons = Array.from(document.getElementsByClassName("delete"));

file_input.addEventListener("change", () => {
  const form = document.getElementById("file-form");
  form.submit();
});

download_buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const file_name =
      button.parentNode.parentNode.children[0].children[0].innerHTML;
    const csrf_token = get_csrf_token();

    if (csrf_token == null) {
      throw Error("CSRF token must be set.");
    }

    headers = {
      "Content-Type": "appliaction/json",
      "X-CSRFToken": csrf_token,
    };
    body = JSON.stringify({ filename: file_name });

    fetch("file/download", {
      method: "POST",
      headers: headers,
      body: body,
    })
      .then((response) => {
        if (!response.ok) {
          throw Error("Failed to initiate file download.");
        }
        return response.blob();
      })
      .then((blob) => handle_blob(blob, file_name))
      .catch((error) => console.error("Error:", error));
  });
});

delete_buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const list_element = button.parentNode.parentNode;
    const file_name = list_element.children[0].children[0].innerHTML;
    const csrf_token = get_csrf_token();

    if (csrf_token == null) {
      throw Error("CSRF token must be set.");
    }

    headers = {
      "Content-Type": "appliaction/json",
      "X-CSRFToken": csrf_token,
    };
    body = JSON.stringify({ filename: file_name });

    fetch("file/delete", {
      method: "POST",
      headers: headers,
      body: body,
    })
      .then((response) => {
        if (!response.ok) {
          throw Error("Failed to delete the file.");
        }
        list_element.parentNode.removeChild(list_element);
      })
      .catch((error) => console.error("Error:", error));
  });
});

function get_csrf_token() {
  const cookies = document.cookie.split(";");
  var csrf_token = null;
  cookies.forEach((cookie) => {
    const parts = cookie.split("=");
    if (parts[0] == "csrftoken") {
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
