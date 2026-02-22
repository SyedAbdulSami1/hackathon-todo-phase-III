# Tailwind Components Prompt

## Context
User wants to create reusable UI components using Tailwind CSS classes.

## Instructions
1. Analyze component requirements
2. Design component structure
3. Create base styles with Tailwind
4. Add variants (size, color, state)
5. Implement responsive variants
6. Add accessibility features
7. Create usage examples

## Output
- Component CSS classes
- Component file (React/Vue/Svelte)
- Variant definitions
- Props interface/types
- Usage examples
- Responsive variants

## Examples
Button component:
```jsx
// Button.jsx
const Button = ({ variant = 'primary', size = 'md', children, ...props }) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2'

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500'
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }

  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]}`

  return (
    <button className={classes} {...props}>
      {children}
    </button>
  )
}
```

Card component:
```jsx
// Card.jsx
const Card = ({ className, children, ...props }) => {
  return (
    <div className={`bg-white rounded-lg shadow-md overflow-hidden ${className}`} {...props}>
      {children}
    </div>
  )
}

const CardHeader = ({ className, children, ...props }) => {
  return (
    <div className={`px-6 py-4 border-b border-gray-200 ${className}`} {...props}>
      {children}
    </div>
  )
}

const CardContent = ({ className, children, ...props }) => {
  return (
    <div className={`px-6 py-4 ${className}`} {...props}>
      {children}
    </div>
  )
}
```

## Questions to Ask
- What type of component do you want? (button, card, form, navigation, etc.)
- What variants are needed? (size, color, state)
- Should it be responsive?
- What framework are you using? (React, Vue, Svelte, etc.)
- Do you need any specific icons or images?
- Are there any accessibility requirements?