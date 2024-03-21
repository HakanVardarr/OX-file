function registerEventHandlers() {
  const file_input = document.getElementById("file");
  const download_buttons = Array.from(
    document.getElementsByClassName("download")
  );
  const delete_buttons = Array.from(document.getElementsByClassName("delete"));

  file_input.addEventListener("change", async () => {
    const form = document.getElementById("file-form");
    const form_data = new FormData(form);

    fetch("file/upload", {
      method: "POST",
      body: form_data,
    })
      .then(async (response) => {
        if (response.ok) {
          return await response.json();
        }
      })
      .then((json) => {
        const date = new Date(json.uploaded_at);
        const options = {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "numeric",
          minute: "numeric",
          hour12: true,
          timeZone: "UTC",
        };

        const formatted_date = date.toLocaleString("en-US", options);

        const file_inner_html = `
        <li class="flex align-center justify-between list-style-none file-list-element">
          <div "file-part">
            <p>${json.filename}</p>
            <p class="file-date">Uploaded at: ${formatted_date} UTC</p>
          </div>
          <div class="flex">
            <button class="large button download">Download</button>
            <button class="large button delete">X</button>
          </div>
        </li>
      `;

        const file_list = document.getElementsByClassName("file-list")[0];

        if (file_list == undefined) {
          const csrf_token = document.querySelector(
            'input[name="csrfmiddlewaretoken"]'
          ).value;
          const form = `
        <li class="flex align-center justify-center file-list-element">
          <form method="post" enctype="multipart/form-data" class="file-form" action="/file/upload" id="file-form">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
            <label for="file" class="flex align-center justify-center large button file">Upload</label>
            <input type="file" name="file" id="file">
          </form>
        </li>
        `;
          var content = document.getElementsByClassName("content")[0];
          document.body.removeChild(content);

          content = document.createElement("div");
          content.className = "content non-empty-content";

          const file_list = document.createElement("ul");
          file_list.className = "file-list";

          file_list.innerHTML += form;
          file_list.innerHTML += file_inner_html;

          content.appendChild(file_list);

          document.body.appendChild(content);
        } else {
          file_list.innerHTML += file_inner_html;
        }

        registerEventHandlers();
      })
      .catch((error) => console.error(error));
  });

  download_buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const file_name =
        button.parentNode.parentNode.children[0].children[0].innerHTML;
      const csrf_token = get_csrf_token();

      if (csrf_token == null) {
        throw Error("CSRF token must be set.");
      }

      const headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      };
      const body = JSON.stringify({ filename: file_name });

      fetch("file/download", {
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
  });

  delete_buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const parent = button.parentNode.parentNode;
      const file_name = parent.children[0].children[0].innerHTML;
      const csrf_token = get_csrf_token();

      if (csrf_token == null) {
        throw Error("CSRF token must be set.");
      }

      const headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      };
      const body = JSON.stringify({ filename: file_name });

      fetch("file/delete", {
        method: "POST",
        headers: headers,
        body: body,
      })
        .then((response) => {
          if (!response.ok) {
            throw Error("Failed to delete the file.");
          }

          const bigger_parent = parent.parentElement;
          bigger_parent.removeChild(parent);

          if (bigger_parent.childElementCount == 1) {
            const content = document.createElement("div");
            content.className = "flex align-center justify-center content";

            const csrf_token = document.querySelector(
              'input[name="csrfmiddlewaretoken"]'
            ).value;
            const form = `
            <div class="upload">
              <h1>Start by uploading your first file</h1>
              <form method="post" enctype="multipart/form-data" class="flex justify-center file-form" action="/file/upload" id="file-form">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                <label for="file" class="flex align-center justify-center large button file">Upload</label>
                <input type="file" name="file" id="file">
              </form>
            </div>
            `;

            content.innerHTML += form;

            bigger_parent.parentNode.remove();
            document.body.appendChild(content);

            registerEventHandlers();
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
}

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

registerEventHandlers();
