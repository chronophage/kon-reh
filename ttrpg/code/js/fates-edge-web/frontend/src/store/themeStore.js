// frontend/src/store/themeStore.js
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Define theme configurations
const themes = {
  fate: {
    name: "Fate's Edge",
    primary: '#8B5CF6',      // Purple
    secondary: '#7C3AED',    // Darker Purple
    accent: '#A78BFA',       // Light Purple
    background: '#111827',   // Dark Gray
    darker: '#0F172A',       // Even Darker
    dark: '#1E293B',         // Dark
    text: '#F1F5F9',         // Light Gray
    textSecondary: '#94A3B8' // Medium Gray
  },
  cyber: {
    name: "Cyberpunk",
    primary: '#00FF99',      // Neon Green
    secondary: '#00CC77',    // Darker Neon
    accent: '#00FFCC',       // Cyan
    background: '#0A0A0A',   // Black
    darker: '#000000',       // Pure Black
    dark: '#1A1A1A',         // Dark Gray
    text: '#E0E0E0',         // Light Gray
    textSecondary: '#888888' // Medium Gray
  },
  fantasy: {
    name: "Fantasy",
    primary: '#D97706',      // Gold
    secondary: '#B45309',    // Darker Gold
    accent: '#F59E0B',       // Amber
    background: '#131B24',   // Deep Blue
    darker: '#0F1720',       // Darker Blue
    dark: '#1E293B',         // Slate
    text: '#F8FAFC',         // Off White
    textSecondary: '#94A3B8' // Blue Gray
  },
  classic: {
    name: "Classic",
    primary: '#3B82F6',      // Blue
    secondary: '#2563EB',    // Darker Blue
    accent: '#60A5FA',       // Light Blue
    background: '#0F172A',   // Dark Blue
    darker: '#020617',       // Very Dark Blue
    dark: '#1E293B',         // Dark
    text: '#F1F5F9',         // Light Gray
    textSecondary: '#94A3B8' // Medium Gray
  }
};

const useThemeStore = create(
  persist(
    (set, get) => ({
      currentTheme: 'fate',
      themes: themes,
      customThemes: {},
      
      // Get current theme configuration
      getTheme: () => {
        const { currentTheme, themes, customThemes } = get();
        return {
          ...themes.fate, // Default to fate theme
          ...(themes[currentTheme] || {}),
          ...(customThemes[currentTheme] || {})
        };
      },
      
      // Change theme
      setTheme: (themeName) => {
        set({ currentTheme: themeName });
        get().applyTheme(themeName);
      },
      
      // Apply theme to document
      applyTheme: (themeName) => {
        const theme = get().getTheme();
        const root = document.documentElement;
        
        root.style.setProperty('--fate-primary', theme.primary);
        root.style.setProperty('--fate-secondary', theme.secondary);
        root.style.setProperty('--fate-accent', theme.accent);
        root.style.setProperty('--fate-background', theme.background);
        root.style.setProperty('--fate-darker', theme.darker);
        root.style.setProperty('--fate-dark', theme.dark);
        root.style.setProperty('--fate-text', theme.text);
        root.style.setProperty('--fate-text-secondary', theme.textSecondary);
      },
      
      // Create custom theme
      createCustomTheme: (name, themeData) => {
        set(state => ({
          customThemes: {
            ...state.customThemes,
            [name]: themeData
          }
        }));
      },
      
      // Initialize theme on app load
      initTheme: () => {
        const { currentTheme } = get();
        get().applyTheme(currentTheme);
      }
    }),
    {
      name: 'fate-edge-theme',
      partialize: (state) => ({ 
        currentTheme: state.currentTheme,
        customThemes: state.customThemes
      })
    }
  )
);

export { useThemeStore, themes };

