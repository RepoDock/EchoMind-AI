const path = require("path");
const { execFile } = require("child_process");

const INSTALLER_PATH = path.join(
    process.env.TEMP,
    "OllamaSetup.exe"
);

async function installOllama(updateStatus) {

    updateStatus("Installing Ollama...");

    await new Promise((resolve, reject) => {

        execFile(

            INSTALLER_PATH,

            [
                "/VERYSILENT",
                "/SUPPRESSMSGBOXES",
                "/NORESTART"
            ],

            (error) => {

                if (error) {
                    reject(error);
                    return;
                }

                resolve();

            }

        );

    });

}

module.exports = {
    installOllama
};