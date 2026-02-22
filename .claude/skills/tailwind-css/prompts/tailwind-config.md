# Tailwind Configuration Prompt

## Context
User wants to configure Tailwind CSS with custom settings, plugins, themes, and extensions.

## Instructions
1. Analyze current Tailwind config (if exists)
2. Determine requirements for configuration
3. Configure theme (colors, fonts, spacing, etc.)
4. Add plugins as needed
5. Set up custom utilities and variants
6. Configure JIT/Purge options
7. Set up dark mode if needed

## Output
- Updated tailwind.config.js
- Plugin installations
- Custom utility definitions
- Variant configurations
- Theme color palette
- Dark mode setup

## Examples
Basic config:
```js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: '#FF6B6B',
        accent: '#4ECDC4',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

With plugins:
```js
module.exports = {
  content: [...],
  theme: {
    extend: {
      // ...
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

## Questions to Ask
- What color scheme do you want to use?
- Do you need any specific plugins? (forms, typography, aspect-ratio, etc.)
- Do you want dark mode? (class, media, or system preference)
- What custom utilities do you need?
- What breakpoints do you want to use?
- Do you need to extend spacing, typography, or other theme properties?