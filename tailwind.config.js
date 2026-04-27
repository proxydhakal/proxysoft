/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: { poppins: ["Poppins", "sans-serif"] },
      colors: {
        // Public site palette
        brand: {
          50: "#eff8ff",
          100: "#dbeffe",
          200: "#bfe3fe",
          300: "#93d1fd",
          400: "#60b6fa",
          500: "#3b97f6",
          600: "#2579eb",
          700: "#1d63d8",
          800: "#1e50af",
          900: "#1e448a"
        },
        // IAM admin palette (kept for existing classes)
        proxyDark: "#0a1d37",
        proxyBlue: "#1e40af",
        proxyCyan: "#38bdf8",
        proxySilver: "#94a3b8"
      },
      animation: {
        float: "float 6s ease-in-out infinite",
        float2: "float 8s ease-in-out infinite 1s",
        float3: "float 7s ease-in-out infinite 2s",
        "pulse-slow": "pulse 4s ease-in-out infinite",
        "spin-slow": "spin 20s linear infinite",
        gradient: "gradientShift 8s ease infinite",
        "slide-up": "slideUp 0.6s ease forwards",
        "fade-in": "fadeIn 0.8s ease forwards"
      },
      keyframes: {
        float: {
          "0%,100%": { transform: "translateY(0px) rotate(0deg)" },
          "50%": { transform: "translateY(-20px) rotate(5deg)" }
        },
        gradientShift: {
          "0%,100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" }
        },
        slideUp: {
          from: { opacity: "0", transform: "translateY(40px)" },
          to: { opacity: "1", transform: "translateY(0)" }
        },
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" }
        }
      },
      backdropBlur: { xs: "2px" }
    }
  }
};

