(function () {
    function protectEmidafReports() {
        const path = window.location.pathname || "";

        if (!path.includes("/reports")) {
            return;
        }

        document.documentElement.setAttribute(
            "translate",
            "no"
        );

        document.documentElement.classList.add(
            "notranslate"
        );

        if (document.body) {
            document.body.setAttribute(
                "translate",
                "no"
            );

            document.body.classList.add(
                "notranslate"
            );
        }

        let meta = document.querySelector(
            'meta[name="google"]'
        );

        if (!meta) {
            meta = document.createElement(
                "meta"
            );

            meta.setAttribute(
                "name",
                "google"
            );

            document.head.appendChild(
                meta
            );
        }

        meta.setAttribute(
            "content",
            "notranslate"
        );
    }

    protectEmidafReports();

    document.addEventListener(
        "DOMContentLoaded",
        protectEmidafReports
    );

    window.addEventListener(
        "popstate",
        protectEmidafReports
    );

    const observer = new MutationObserver(
        protectEmidafReports
    );

    observer.observe(
        document.documentElement,
        {
            childList: true,
            subtree: true
        }
    );
})();
