async function sendMessage() {

    let username =
        document.getElementById("username").value.trim();

    let message =
        document.getElementById("message").value.trim();

    let recipient =
        document.getElementById("recipient").value;

    if (username === "" || message === "") {

        alert("Please enter username and message");
        return;
    }

    // Lock username after first message
    let usernameField =
        document.getElementById("username");

    if (!usernameField.disabled) {

        usernameField.disabled = true;

        usernameField.style.backgroundColor =
            "#e9ecef";

        usernameField.style.cursor =
            "not-allowed";

        usernameField.title =
            "Username cannot be changed";

        document.getElementById("current-user")
            .innerText = username;
    }

    try {

        let response = await fetch("/send", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                username: username,

                message: message,

                recipient: recipient

            })

        });

        if (!response.ok) {

            throw new Error("Failed to send message");
        }

        document.getElementById("message").value = "";

        loadMessages();

    } catch (error) {

        console.error(error);

        alert("Message could not be sent.");
    }
}

function updateRecipientList(users) {

    let recipient =
        document.getElementById("recipient");

    let currentSelection =
        recipient.value;

    recipient.innerHTML =
        '<option value="ALL">Send to All</option>';

    users.forEach(user => {

        let option =
            document.createElement("option");

        option.value = user;

        option.textContent =
            "Send to " + user;

        recipient.appendChild(option);
    });

    // Restore previous selection if possible
    if ([...recipient.options].some(
        option => option.value === currentSelection
    )) {

        recipient.value = currentSelection;

    } else {

        recipient.value = "ALL";
    }
}

async function loadUsers() {

    try {

        let response =
            await fetch("/users");

        let users =
            await response.json();

        let list =
            document.getElementById("users-list");

        list.innerHTML = "";

        users.forEach(user => {

            let li =
                document.createElement("li");

            li.innerHTML =
                " " + user;

            list.appendChild(li);
        });

        updateRecipientList(users);

    } catch (error) {

        console.error(
            "Failed loading users:",
            error
        );
    }
}

async function loadMessages() {

    let username =
        document.getElementById("username")
        .value.trim();

    if (username === "")
        return;

    try {

        let response =
            await fetch(
                "/messages?user=" +
                encodeURIComponent(username)
            );

        let messages =
            await response.json();

        let chatBox =
            document.getElementById("chat-box");

        chatBox.innerHTML = "";

        // Welcome Message
        let welcome =
            document.createElement("div");

        welcome.className =
            "message system";

        welcome.innerHTML =
            "Welcome to Chatroom";

        chatBox.appendChild(welcome);

        messages.forEach(msg => {

            let div =
                document.createElement("div");

            // PRIVATE MESSAGE
            if (msg.type === "private") {

                div.className =
                    "message private";

                div.innerHTML =
                    "<b>" +
                    msg.from +
                    "</b> to <b>" +
                    msg.to +
                    "</b>: " +
                    msg.text;
            }

            // PUBLIC MESSAGE
            else {

                div.className =
                    "message user";

                div.innerHTML =
                    "<b>" +
                    msg.from +
                    "</b>: " +
                    msg.text;
            }

            chatBox.appendChild(div);
        });

        chatBox.scrollTop =
            chatBox.scrollHeight;

    } catch (error) {

        console.error(
            "Failed loading messages:",
            error
        );
    }
}

/* Show username in top-right box while typing */

document
.getElementById("username")
.addEventListener("input", function () {

    let username =
        this.value.trim();

    document.getElementById("current-user")
        .innerText =
        username || "Not Set";
});

/* Send message on Enter key */

document
.getElementById("message")
.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {

        sendMessage();
    }
});

/* Initial Load */

loadUsers();
loadMessages();

/* Auto Refresh */

setInterval(loadUsers, 1000);
setInterval(loadMessages, 1000);