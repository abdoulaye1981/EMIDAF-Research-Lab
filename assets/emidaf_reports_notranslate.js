(function () {
    function lockTranslation() {
        const pathname = window.location.pathname || "";

        if (!pathname.includes("/reports")) {
            return;
        }

        document.documentElement.lang = "fr";
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

        document
            .querySelectorAll("*")
            .forEach(function (element) {
                element.setAttribute(
                    "translate",
                    "no"
                );
            });

        let meta = document.querySelector(
            'meta[name="google"]'
        );

        if (!meta) {
            meta = document.createElement(
                "meta"
            );
            meta.name = "google";
            document.head.appendChild(
                meta
            );
        }

        meta.content = "notranslate";
    }

    lockTranslation();

    document.addEventListener(
        "DOMContentLoaded",
        lockTranslation
    );

    const observer = new MutationObserver(
        lockTranslation
    );

    observer.observe(
        document.documentElement,
        {
            childList: true,
            subtree: true
        }
    );
})();
