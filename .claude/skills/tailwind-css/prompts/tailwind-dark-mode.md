# Tailwind Dark Mode Prompt

## Context
User wants to implement dark mode in their Tailwind CSS project.

## Instructions
1. Determine dark mode strategy (class, media, system)
2. Configure dark mode in Tailwind
3. Create dark mode variants
4. Implement theme toggle
5. Add system preference detection
6. Create smooth transitions
7. Test dark mode implementation

## Output
- Dark mode configuration
- Dark variant classes
- Theme toggle component
- System preference detection
- Transition utilities
- Dark mode examples

## Examples
Configuration:
```js
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#1a202c',
          text: '#e2e8f0',
          primary: '#4299e1',
        }
      }
    }
  }
}
```

Dark variants:
```html
<!-- Using dark: prefix -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Dark mode content
</div>

<button class="bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700">
  Button
</button>
```

Theme toggle component:
```jsx
// ThemeToggle.jsx
import { useState, useEffect } from 'react'

const ThemeToggle = () => {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    const isDarkMode = localStorage.getItem('darkMode') === 'true' ||
      (!('darkMode' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)

    setIsDark(isDarkMode)
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  const toggleTheme = () => {
    const newDarkMode = !isDark
    setIsDark(newDarkMode)

    if (newDarkMode) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('darkMode', 'true')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('darkMode', 'false')
    }
  }

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 transition-colors"
    >
      {isDark ? '☀️' : '🌙'}
    </button>
  )
}
```

System preference detection:
```js
// Detect system preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

// Listen for changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  const newPrefersDark = e.matches
  // Update theme based on system preference
})
```

## Questions to Ask
- How should dark mode be triggered? (manual toggle, system preference, both)
- Should it use the 'class' strategy or 'media' query?
- Do you need a theme toggle component?
- Should dark mode be persisted in localStorage?
- Do you need different color schemes for light/dark modes?
- Should there be smooth transitions between themes?