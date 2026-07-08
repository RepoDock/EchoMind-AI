const { exec } = require("child_process");
const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");
function getDefaultOllamaPath() {

    return path.join(
        os.homedir(),
        "AppData",
        "Local",
        "Programs",
        "Ollama",
        "ollama.exe"
    );

}
function getOllamaExecutable() {

    const defaultPath = getDefaultOllamaPath();

    if (fs.existsSync(defaultPath)) {
        return defaultPath;
    }

    return "ollama";

}
function checkOllama() {
    return new Promise((resolve) => {

        exec("ollama --version", (error, stdout, stderr) => {


            if (error) {

                const defaultPath = getDefaultOllamaPath();

                if (fs.existsSync(defaultPath)) {

                    resolve({
                        installed: true,
                        version: "Unknown",
                        error: null
                    });

                    return;

                }

                resolve({
                    installed: false,
                    version: null,
                    error: error.message
                });

                return;
            }

            const output = `${stdout}\n${stderr}`;

            const match = output.match(/\d+\.\d+\.\d+/);

            resolve({
                installed: true,
                version: match ? match[0] : "Unknown",
                error: null
            });

        });

    });
}
function checkOllamaServer() {
    return new Promise((resolve) => {

        http.get("http://127.0.0.1:11434/api/tags", (res) => {

            resolve(true);

        }).on("error", () => {

            resolve(false);

        });

    });
}

module.exports = {
    checkOllama,
    checkOllamaServer,
    getOllamaExecutable
};