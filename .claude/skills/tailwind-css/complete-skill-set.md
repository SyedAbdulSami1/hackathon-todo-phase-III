# Tailwind CSS Complete Skill Set

## Overview
Comprehensive skill set for Tailwind CSS covering all aspects of the framework from basic setup to advanced patterns.

## Core Skills

### 1. Setup & Configuration
- **tailwind-install**: Install Tailwind CSS and dependencies
- **tailwind-init**: Initialize Tailwind configuration
- **tailwind-config**: Configure Tailwind with custom settings
- **tailwind-plugins**: Add and configure Tailwind plugins

### 2. Layout & Spacing
- **tailwind-flexbox**: Create flexible layouts with flexbox
- **tailwind-grid**: Build complex layouts with CSS Grid
- **tailwind-spacing**: Manage padding, margin, and spacing
- **tailwind-sizing**: Control element dimensions and sizing

### 3. Typography
- **tailwind-fonts**: Configure and use font families and weights
- **tailwind-text**: Style text with size, color, and alignment
- **tailwind-leading**: Control line height and leading
- **tailwind-tracking**: Adjust letter and word spacing

### 4. Colors & Themes
- **tailwind-colors**: Use and customize color palettes
- **tailwind-dark-mode**: Implement dark mode variants
- **tailwind-themes**: Create and manage design themes
- **tailwind-accessible-colors**: Ensure color accessibility

### 5. Visual Effects
- **tailwind-shadows**: Apply box and text shadows
- **tailwind-borders**: Style borders and dividers
- **tailwind-radius**: Control border radius and shapes
- **tailwind-opacity**: Manage transparency and opacity

### 6. Responsive Design
- **tailwind-breakpoints**: Define and use responsive breakpoints
- **tailwind-mobile-first**: Implement mobile-first responsive design
- **tailwind-container**: Control container widths and centering
- **tailwind-hidden**: Show/hide elements responsively

### 7. States & Interactions
- **tailwind-hover**: Style elements on hover state
- **tailwind-focus**: Style elements on focus state
- **tailwind-active**: Style elements on active state
- **tailwind-disabled**: Style disabled elements

### 8. Animations & Transitions
- **tailwind-transitions**: Add smooth property transitions
- **tailwind-animations**: Create and use CSS animations
- **tailwind-transforms**: Apply transforms and rotations
- **tailwind-motion**: Create motion-friendly designs

### 9. Forms & Inputs
- **tailwind-forms**: Style form elements and inputs
- **tailwind-buttons**: Create styled buttons
- **tailwind-inputs**: Style various input types
- **tailwind-validation**: Style form validation states

### 10. Components & Patterns
- **tailwind-cards**: Create card components
- **tailwind-navigation**: Build navigation components
- **tailwind-modals**: Create modal dialogs
- **tailwind-accordions**: Build accordion components

### 11. Performance & Optimization
- **tailwind-purge**: Configure purging for production
- **tailwind-jit**: Use Just-In-Time mode
- **tailwind-optimization**: Optimize Tailwind usage
- **tailwind-utilities**: Create custom utility classes

### 12. Framework Integration
- **tailwind-nextjs**: Integrate with Next.js
- **tailwind-react**: Use with React components
- **tailwind-vue**: Use with Vue.js
- **tailwind-svelte**: Use with Svelte

## Usage Patterns

### Quick Start
```
/tailwind-install --framework=nextjs
/tailwind-config --plugins=forms,typography
/tailwind-dark-mode --strategy=class
```

### Component Creation
```
/tailwind-buttons --variants=primary,secondary,ghost
/tailwind-cards --variants=elevated,outlined
/tailwind-forms --theme=modern
```

### Responsive Design
```
/tailwind-breakpoints --custom=xs:475,3xl:1600
/tailwind-mobile-first --layout=sidebar,content
/tailwind-hidden --responsive=sm:hidden,md:block
```

### Advanced Features
```
/tailwind-animations --preset=fade-in,slide-up
/tailwind-themes --create=light,dark,system
/tailwind-optimization --mode=jit,purge
```

## Best Practices

### Naming Conventions
- Use semantic class combinations
- Group related classes logically
- Follow mobile-first ordering
- Maintain consistent spacing

### Performance Tips
- Use JIT mode in development
- Configure proper purging for production
- Limit arbitrary values
- Use component classes when appropriate

### Accessibility Considerations
- Maintain sufficient color contrast
- Support focus states for keyboard navigation
- Use appropriate aria attributes
- Consider reduced motion preferences

### Maintenance Guidelines
- Document custom configurations
- Create reusable component classes
- Use consistent color naming
- Regularly audit unused classes

## Troubleshooting

### Common Issues
- Missing styles in production (purge configuration)
- Responsive breakpoints not working (mobile-first approach)
- Dark mode not applying (class strategy vs media query)
- JIT mode conflicts (plugin compatibility)

### Debugging Steps
1. Verify Tailwind configuration
2. Check content paths in config
3. Confirm build process integration
4. Test in isolated environment