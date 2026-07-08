const { spawn } = require("child_process");
const { getOllamaExecutable } = require("./checkOllama.cjs");

let ollamaProcess = null;

async function startOllama() {

    if (ollamaProcess) {
        return;
    }

    ollamaProcess = spawn(getOllamaExecutable(), ["serve"], {
        detached: true,
        windowsHide: true,
        shell: false,
        stdio: "ignore"
    });

    ollamaProcess.on("error", (err) => {
        console.error("Failed to start Ollama:", err);
        ollamaProcess = null;
    });

    ollamaProcess.unref();

}

module.exports = {
    startOllama
};