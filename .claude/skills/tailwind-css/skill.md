# Tailwind CSS Skills

## Overview
Comprehensive Tailwind CSS skills covering configuration, utilities, components, patterns, and best practices for modern web development.

## Available Skills

### 1. Tailwind Configuration
- **tailwind-setup**: Initialize Tailwind CSS in a project
- **tailwind-config**: Configure Tailwind with custom settings, plugins, and themes
- **tailwind-extend**: Extend Tailwind with custom utilities, components, and variants

### 2. Utility Classes
- **tailwind-utilities**: Generate and use utility classes for styling
- **tailwind-responsive**: Apply responsive design utilities (mobile-first, breakpoints)
- **tailwind-states**: Use pseudo-classes and state variants (hover, focus, active, etc.)
- **tailwind-layout**: Create layouts with flexbox and grid utilities

### 3. Components
- **tailwind-components**: Create reusable UI components with Tailwind
- **tailwind-theming**: Implement design systems and themes with Tailwind
- **tailwind-dark-mode**: Configure and use dark mode variants
- **tailwind-variants**: Create variant-based components with conditional styling

### 4. Advanced Patterns
- **tailwind-animation**: Create and use custom animations and transitions
- **tailwind-effects**: Apply visual effects (shadows, gradients, filters, blends)
- **tailwind-typography**: Configure and use the typography plugin
- **tailwind-forms**: Style forms with Tailwind Forms plugin

### 5. Performance & Optimization
- **tailwind-purge**: Configure and use PurgeCSS/JIT for production builds
- **tailwind-optimization**: Optimize Tailwind for performance
- **tailwind-arbitrary-values**: Use arbitrary values effectively
- **tailwind-custom-css**: Integrate custom CSS with Tailwind

### 6. Integration
- **tailwind-nextjs**: Integrate Tailwind with Next.js
- **tailwind-react**: Use Tailwind with React components
- **tailwind-vue**: Use Tailwind with Vue.js
- **tailwind-svelte**: Use Tailwind with Svelte

### 7. Best Practices
- **tailwind-bem**: Apply BEM methodology with Tailwind
- **tailwind-architecture**: Organize Tailwind code in large projects
- **tailwind-migration**: Migrate from CSS frameworks to Tailwind
- **tailwind-guidelines**: Follow Tailwind best practices and conventions

## Usage Examples

### Basic Setup
```bash
# Initialize Tailwind CSS
/tailwind-setup --project=nextjs --css=app/globals.css
```

### Configuration
```bash
# Configure Tailwind
/tailwind-config --add-plugin=forms,typography --extend-colors=brand,accent
```

### Creating Components
```bash
# Create a reusable button component
/tailwind-components --name=Button --variants=size,color --states=hover,focus
```

### Responsive Design
```bash
# Apply responsive utilities
/tailwind-responsive --mobile-first --breakpoints=sm,md,lg,xl
```

## Prerequisites
- Node.js and npm/yarn installed
- Basic knowledge of CSS and HTML
- Familiarity with modern build tools (Vite, Webpack, etc.)

## Output Format
All Tailwind skills return:
1. **Configuration updates** (tailwind.config.js, postcss.config.js)
2. **CSS code** (utility classes, component styles)
3. **Implementation examples** (React, Vue, Svelte components)
4. **Best practices** for the specific use case
5. **Performance considerations**