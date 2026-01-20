document.addEventListener("DOMContentLoaded", function () {
    const consent = localStorage.getItem("cookie_consent");

    if (!consent) {
        const modal = new bootstrap.Modal(
            document.getElementById("cookieConsentModal"),
            { backdrop: "static", keyboard: false }
        );
        modal.show();
    }

    document.getElementById("acceptCookies")?.addEventListener("click", function () {
        localStorage.setItem("cookie_consent", "accepted");
        location.reload(); // reload to activate cookies/scripts
    });

    document.getElementById("rejectCookies")?.addEventListener("click", function () {
        localStorage.setItem("cookie_consent", "rejected");
        location.reload();
    });
});