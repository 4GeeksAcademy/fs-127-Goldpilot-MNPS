/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF",
        secondary: "#9333EA",
        accent: "#F59E0B",
        brand: {
          light: "#3B82F6",
          DEFAULT: "#2563EB",
          dark: "#1E3A8A",
        },
      },
    },
  },
  plugins: [],
};
