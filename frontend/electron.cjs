const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const http = require("http");
let backend;
let splash;
let mainWindow;
const isDev = !app.isPackaged;
const {
    dependencyManager
} = require("./startup/dependencyManager.cjs");
async function createSplash() {

    splash = new BrowserWindow({
        width: 500,
        height: 400,
        frame: false,
        resizable: false,
        alwaysOnTop: true,
        autoHideMenuBar: true,
        transparent: false,
        show: true,
        backgroundColor: "#0B1020",
        center: true
    });

    await splash.loadFile(path.join(__dirname, "loading.html"));

}
function updateSplashStatus(message) {

    if (!splash || splash.isDestroyed()) return;
    if (splash.webContents.isLoading()) return;

    const percent = (message.match(/(\d+)%/) || [])[1] || "0";

    splash.webContents.executeJavaScript(`
        (() => {

            const status = document.getElementById("status");
            const progress = document.querySelector(".progress");
            const fill = document.getElementById("progressFill");

            if(status){
                status.innerText = ${JSON.stringify(message)};
            }

            if(progress && fill){

                if(${percent} > 0){

                    progress.style.display = "block";
                    fill.style.width = "${percent}%";

                }else{

                    progress.style.display = "none";
                    fill.style.width = "0%";

                }

            }

        })();
    `).catch(console.error);

}
function waitForBackend() {
    return new Promise((resolve) => {

        const check = () => {

            http.get("http://127.0.0.1:8000", () => {
                resolve();
            }).on("error", () => {
                setTimeout(check, 500);
            });

        };

        check();

    });
}
// function waitForBackend(timeout = 30000) {
    
//     return new Promise((resolve, reject) => {

//         const start = Date.now();

//         const check = () => {


//             http.get("http://127.0.0.1:8000", (res) => {

//                 console.log("Backend HTTP Status:", res.statusCode);

//                 resolve();

//             }).on("error", (err) => {

//                 console.log("Waiting for backend:", err.code);

//                 if (Date.now() - start > timeout) {

//                     reject(new Error("Backend failed to start."));

//                     return;
//                 }

//                 setTimeout(check, 30000);

//             });

//         };

//         check();

//     });

// }
function createWindow() {

    mainWindow = new BrowserWindow({
        width: 1500,
        height: 900,
        show: false,
        autoHideMenuBar: true,

        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    if (isDev) {
        mainWindow.loadURL("http://localhost:5173");
    } else {
        mainWindow.loadFile(
            path.join(__dirname, "dist", "index.html")
        );
    }

    if (isDev) {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.webContents.on("did-finish-load", () => {

        console.log("Frontend Loaded");
        updateSplashStatus("Almost Ready...");
        mainWindow.show();

        if (splash && !splash.isDestroyed()) {
            splash.close();
        }

    });

    mainWindow.webContents.on("did-fail-load", (_, code, desc) => {
        console.log(code, desc);
    });
}

app.whenReady().then(async () => {
    await createSplash();

    try {

        const ready = await dependencyManager(updateSplashStatus);

        if (!ready) {
            return;
        }

    } catch (err) {

        console.error(err);

        updateSplashStatus("Failed to start AI Engine.");

        return;

    }

    updateSplashStatus("Starting Backend...");

    

    const backendPath = isDev
        ? path.join(
            __dirname,
            "../backend/dist/AXONBackend.exe"
        )
        : path.join(
            process.resourcesPath,
            "backend",
            "AXONBackend.exe"
        );

    backend = spawn(backendPath, [], {
        cwd: path.dirname(backendPath),
        windowsHide: !isDev,
        stdio: "pipe",
        detached: false
    });

    backend.stdout.on("data", (data) => {
        console.log("[Backend]", data.toString().trim());
    });

    backend.stderr.on("data", (data) => {
        console.error("[Backend Error]", data.toString().trim());
    });

    backend.on("error", (err) => {
        console.error("Spawn Error:", err);
    });

    backend.on("exit", (code, signal) => {
        console.log("EXIT:", code, signal);
    });

    console.log("Backend Path:", backendPath);

    backend.on("spawn", () => {
        console.log(" Backend Spawned");
    });




    // console.log("Skipping backend check");
    // createWindow();
    try {

        await waitForBackend();

        console.log("Backend Ready");

        updateSplashStatus("Opening Workspace...");

        createWindow();

    } catch (err) {

        console.error(err);

        updateSplashStatus("Backend failed to start.");

    }

});

app.on("window-all-closed", () => {

    if (backend && !backend.killed) {
        backend.kill();
    }

    app.quit();

});
