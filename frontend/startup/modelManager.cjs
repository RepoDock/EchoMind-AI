const http = require("http");
const { exec, spawn } = require("child_process");
const { getOllamaExecutable } = require("./checkOllama.cjs");
const REQUIRED_MODELS = [
    "qwen2.5:7b",
    "nomic-embed-text"
];
function getInstalledModels() {

    return new Promise((resolve, reject) => {

        exec(`"${getOllamaExecutable()}" list`, (error, stdout) => {

            if (error) {
                reject(error);
                return;
            }

            const models = stdout
                .split("\n")
                .slice(1)
                .map(line => line.trim().split(/\s+/)[0])
                .filter(Boolean);

            resolve(models);

        });

    });

}
function pullModelAPI(model, updateStatus) {

    return new Promise((resolve, reject) => {

        const req = http.request({

            hostname: "127.0.0.1",
            port: 11434,
            path: "/api/pull",
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }

        }, (res) => {

            let buffer = "";

            res.on("data", (chunk) => {

                buffer += chunk.toString();

                const lines = buffer.split("\n");

                buffer = lines.pop();

                for (const line of lines) {

                    if (!line.trim()) continue;

                    try {

                        const obj = JSON.parse(line);

                        if (obj.completed && obj.total) {

                            const percent = Math.floor(
                                (obj.completed / obj.total) * 100
                            );

                            const completedGB =
                                (obj.completed / 1024 / 1024 / 1024).toFixed(2);

                            const totalGB =
                                (obj.total / 1024 / 1024 / 1024).toFixed(2);

                            updateStatus(
`Downloading AI Model...

${percent}%

${completedGB} GB / ${totalGB} GB`
                            );

                        }
                        else if (obj.status) {

                            updateStatus(obj.status);

                        }

                    } catch {

                    }

                }

            });

            res.on("end", () => {

                resolve();

            });

        });

        req.on("error", reject);

        req.write(JSON.stringify({

            model

        }));

        req.end();

    });

}
// function pullModel(model, updateStatus) {
//     console.log("PullModel Started");

//     updateStatus("Downloading AI Model...");
//     return new Promise((resolve, reject) => {

//         updateStatus(`Downloading ${model}...`);
//         const process = spawn("ollama", ["pull", model]);

//         // process.stdout.on("data", (data) => {

//         //     console.log(data.toString());

//         // });
//         process.stdout.on("data", (data) => {

//             const text = data
//             .toString()
//             .replace(/\x1B\[[0-9;]*m/g, "");

//             console.log(text);

//             const percent = text.match(/(\d+)%/);

//             const size = text.match(
//                 /(\d+(?:\.\d+)?)\s*(MB|GB)\s*\/\s*(\d+(?:\.\d+)?)\s*(MB|GB)/i
//             );

//             if (percent && size) {

//                 updateStatus(
//                     `Downloading AI Model...

//                     ${percent[1]}%

//                     ${size[1]} ${size[2]} / ${size[3]} ${size[4]}`
//                     );

//             }
//             else if (percent) {

//                 updateStatus(
//                     `Downloading AI Model... ${percent[1]}%`
//                 );

//             }

//         });

//         process.stderr.on("data", (data) => {

//             console.log(data.toString());

//         });

//         // process.stdout.on("data", (data) => {

//         //     const text = data.toString();

//         //     console.log(text);

//         //     const match = text.match(
//         //         /(\d+)%.*?(\d+(\.\d+)?)\s*(MB|GB)\/(\d+(\.\d+)?)\s*(MB|GB)/i
//         //     );

//         //     if (match) {

//         //         updateStatus(

//         // `Downloading AI Model...

//         // ${match[1]}%

//         // ${match[2]} ${match[4]} / ${match[5]} ${match[7]}`

//         //         );

//         //     }

//         // });

//         // process.stderr.on("data", (data) => {

//         //     const text = data.toString();

//         //     console.log("STDERR:", text);

//         // });

//         process.on("exit", (code) => {

//             if (code === 0) {
//                 resolve();
//             } else {
//                 reject(new Error(`Failed to download ${model}`));
//             }

//         });

//     });

// }

async function modelManager(updateStatus) {

    const installed = await getInstalledModels();

    console.log("Installed Models:", installed);

    for (const model of REQUIRED_MODELS) {

        if (!installed.includes(model)) {

            await pullModelAPI(model, updateStatus);

        }

    }

    return true;

}

module.exports = {
    modelManager
};