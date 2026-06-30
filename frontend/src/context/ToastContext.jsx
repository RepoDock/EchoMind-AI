import { createContext, useContext, useState } from "react";
import Toast from "../components/ui/Toast";

const ToastContext = createContext();

export function ToastProvider({ children }) {
  const [toast, setToast] = useState({
    show: false,
    message: "",
    type: "success",
  });

  const showToast = (message, type = "success") => {
    setToast({
      show: true,
      message,
      type,
    });

    setTimeout(() => {
      setToast({
        show: false,
        message: "",
        type: "success",
      });
    }, 2500);
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}

      <Toast
        show={toast.show}
        message={toast.message}
        type={toast.type}
      />
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}