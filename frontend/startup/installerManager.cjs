const fs = require("fs");
const path = require("path");

const { download } = require("./utils/downloader.cjs");
const { installOllama } = require("./installOllama.cjs");
const { checkOllama } = require("./checkOllama.cjs");

const INSTALLER_URL =
    "https://ollama.com/download/OllamaSetup.exe";

const INSTALLER_PATH = path.join(
    process.env.TEMP,
    "OllamaSetup.exe"
);

async function installerManager(updateStatus) {

    if (!fs.existsSync(INSTALLER_PATH)) {

        updateStatus("Downloading Ollama...");

        await download(
            INSTALLER_URL,
            INSTALLER_PATH,
            (progress) => {

                updateStatus(
                    `Downloading Ollama... ${progress}%`
                );

            }
        );

    }

    await installOllama(updateStatus);
    updateStatus("Waiting for installation...");

    const start = Date.now();

    while (Date.now() - start < 120000) {

        const result = await checkOllama();

        if (result.installed) {
            break;
        }

        await new Promise(resolve => setTimeout(resolve, 1000));

    }

    updateStatus("Verifying Installation...");

    const result = await checkOllama();

    if (!result.installed) {

        throw new Error("Ollama installation failed.");

    }

    try {
        fs.unlinkSync(INSTALLER_PATH);
    } catch (_) {}

    return true;

}

module.exports = {
    installerManager
};