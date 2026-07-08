import { createContext, useContext, useEffect, useState } from "react";
import { themes } from "./themes";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(
    localStorage.getItem("theme") || "light"
  );

  useEffect(() => {
    localStorage.setItem("theme", theme);

    const colors = themes[theme].colors;

    document.documentElement.style.setProperty("--bg", colors.bg);
    document.documentElement.style.setProperty("--card", colors.card);
    document.documentElement.style.setProperty("--text", colors.text);
    document.documentElement.style.setProperty("--border", colors.border);
    document.documentElement.style.setProperty("--primary", colors.primary);
  }, [theme]);

  return (
    <ThemeContext.Provider
      value={{
        theme,
        setTheme,
        colors: themes[theme].colors,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}