// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://127.0.0.1:8000",
// });

// export default api;
// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://localhost:8000",
// });

// export default api;
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const scanFolder = (folderPath) => {
  return api.post("/scanner/scan", {
    folder_path: folderPath,
  });
};
export const getFiles = () => {
  return api.get("/files");
};
export const getStats = () => {
  return api.get("/scanner/stats");
};
export const openFile = (path) => {
  return api.post("/files/open", {
    path,
  });
};

export const showInFolder = (path) => {
  return api.post("/files/show", {
    path,
  });
};
export const getRecentFiles = () => {
  return api.get("/recent");
};
export const getFolder = () => {
  return api.get("/settings/folder");
};
export const getScanFolder = () => {
  return api.get("/settings/scan-folder");
};
export const saveFolder = (folder) => {
  return api.post("/settings/folder", {
    folder,
  });
};
export default api;


