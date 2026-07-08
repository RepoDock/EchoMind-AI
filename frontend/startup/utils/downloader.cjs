const fs = require("fs");
const https = require("https");
const http = require("http");

function download(url, destination, onProgress = () => {}) {

    return new Promise((resolve, reject) => {

        const request = (downloadUrl) => {

            const client = downloadUrl.startsWith("https")
                ? https
                : http;

            client.get(downloadUrl, (response) => {

                // Handle Redirects
                if (
                    response.statusCode >= 300 &&
                    response.statusCode < 400
                ) {

                    if (!response.headers.location) {
                        reject(new Error("Redirect location missing."));
                        return;
                    }

                    const nextUrl = new URL(
                        response.headers.location,
                        downloadUrl
                    ).toString();

                    request(nextUrl);
                    return;
                }

                if (response.statusCode !== 200) {

                    reject(
                        new Error(
                            `Download failed (${response.statusCode})`
                        )
                    );

                    return;
                }

                const total = Number(
                    response.headers["content-length"]
                );

                let downloaded = 0;

                const file = fs.createWriteStream(destination);

                response.on("data", (chunk) => {

                    downloaded += chunk.length;

                    if (total > 0) {

                        const progress = Math.floor(
                            (downloaded / total) * 100
                        );

                        onProgress(progress);

                    }

                });

                response.pipe(file);

                file.on("finish", () => {

                    file.close();

                    resolve();

                });

                file.on("error", (err) => {

                    fs.unlink(destination, () => {});

                    reject(err);

                });

            }).on("error", reject);

        };

        request(url);

    });

}

module.exports = {
    download
};