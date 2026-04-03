let isLogin = true;

function toggleForm() {
    isLogin = !isLogin;

    document.getElementById("formTitle").innerText =
        isLogin ? "Login" : "Sign Up";

    document.getElementById("mainBtn").innerText =
        isLogin ? "Login" : "Create Account";

    document.getElementById("toggleText").innerText =
        isLogin ? "Don't have an account?" : "Already have an account?";

    document.getElementById("toggleLink").innerText =
        isLogin ? "Sign Up" : "Login";

    document.getElementById("password").placeholder =
        isLogin ? "Password" : "Create Password";
}

function handleAuth() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const url = isLogin ? "/login" : "/signup";

    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("status").innerText = data.error;
        } else {
            if (isLogin) {
                localStorage.setItem("user_email", email);
                window.location.href = "dashboard.html";
            } else {
                toggleForm();
            }
        }
    });
}

function showSection(event, id) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");

    document.querySelectorAll(".sidebar li").forEach(li => li.classList.remove("active"));
    event.target.classList.add("active");
}

function logout() {
    localStorage.clear();
    window.location.href = "/";
}

function uploadImage() {
    const fileInput = document.getElementById("imageInput");
    const status = document.getElementById("status");
    const preview = document.getElementById("outputPreview");

    if (!fileInput.files.length) {
        status.innerText = "Select image first";
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    status.innerText = "Processing...";

    fetch("/protect", {
        method: "POST",
        body: formData
    })
    .then(res => res.blob())
    .then(blob => {
        preview.src = URL.createObjectURL(blob);
        status.innerText = "Done!";
    });
}
