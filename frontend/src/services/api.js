
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
export const aiSearch = (query) =>
  api.post("/ai/search", {
    query,
  });
export const chatWithAI = (question, history, mode) =>
  api.post("/chat/chat", {
    question,
    history,
    mode,
  });

export const checkSetup = () => api.get("/setup/check");

export const installEngine = () =>
  api.post("/setup/install-engine");

export const downloadModel = () =>
  api.post("/setup/download-model");

export const modelStatus = () =>
  api.get("/setup/model-status");
export const clearData = () =>
  api.post("/scanner/clear-data");

export const showInFolder = (path) => {
  return api.post("/files/show", {
    path,
  });
};
export const browseFolder = () => {
  return api.get("/settings/browse");
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
export const askDocumentAI = (
  fileId,
  question,
  history = []
) =>
  api.post("/chat/document-chat", {
    file_id: fileId,
    question,
    history,
  });

export default api;


