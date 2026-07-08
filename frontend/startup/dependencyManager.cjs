const {
    checkOllama,
    checkOllamaServer
} = require("./checkOllama.cjs");
const {
    startOllama
} = require("./startOllama.cjs");
const {
    installerManager
} = require("./installerManager.cjs");
const {
    modelManager
} = require("./modelManager.cjs");
async function waitForOllama(timeout = 15000) {

    const start = Date.now();

    while (Date.now() - start < timeout) {

        const running = await checkOllamaServer();

        if (running) {
            return true;
        }

        await new Promise(resolve => setTimeout(resolve, 500));

    }

    return false;

}

async function dependencyManager(updateStatus) {

    updateStatus("Checking Ollama...");

    const ollama = await checkOllama();

    console.log("Ollama:", ollama);

    if (!ollama.installed) {

        updateStatus("Ollama not found.");

        await installerManager(updateStatus);

        const verify = await checkOllama();

        if (!verify.installed) {

            throw new Error("Ollama installation failed.");

        }

    }
    
    updateStatus("Checking AI Engine...");

    let running = await checkOllamaServer();

    console.log("Server Running:", running);

    if (!running) {

        updateStatus("Starting AI Engine...");

        await startOllama();

        running = await waitForOllama();

        if (!running) {
            updateStatus("Failed to start AI Engine.");
            throw new Error("Failed to start Ollama.");
        }

        console.log("Ollama Started");

    }

    updateStatus("Checking AI Models...");

    updateStatus("Entered Model Manager...");
    console.log("Before modelManager");

    await modelManager(updateStatus);

    console.log("After modelManager");

    return true;

}

module.exports = {
    dependencyManager
};