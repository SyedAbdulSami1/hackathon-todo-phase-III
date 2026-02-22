# Tailwind Responsive Design Prompt

## Context
User wants to implement responsive design using Tailwind CSS utilities and breakpoints.

## Instructions
1. Analyze layout requirements
2. Identify responsive breakpoints
3. Create mobile-first design
4. Implement responsive utilities
5. Add responsive variants to components
6. Create responsive grid layouts
7. Test on different screen sizes

## Output
- Responsive utility classes
- Breakpoint configuration
- Mobile-first CSS
- Responsive component variants
- Grid layout examples
- Media query alternatives

## Examples
Basic responsive utilities:
```html
<div class="text-center sm:text-left md:text-right lg:text-center">
  Responsive text alignment
</div>

<div class="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
  Responsive width
</div>

<div class="hidden sm:block md:hidden lg:block">
  Show/hide based on breakpoint
</div>
```

Responsive grid:
```html
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <div class="bg-gray-200 p-4">Column 1</div>
  <div class="bg-gray-200 p-4">Column 2</div>
  <div class="bg-gray-200 p-4">Column 3</div>
  <div class="bg-gray-200 p-4">Column 4</div>
</div>
```

Responsive navigation:
```html
<nav class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
  <a href="#" class="text-center sm:text-left">Home</a>
  <a href="#" class="text-center sm:text-left">About</a>
  <a href="#" class="text-center sm:text-left">Contact</a>
</nav>
```

Custom breakpoints:
```js
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      '3xl': '1600px',
      '4xl': '1920px',
    },
  },
}
```

## Questions to Ask
- What are the target breakpoints? (mobile, tablet, desktop)
- Should it be mobile-first or desktop-first?
- Do you need custom breakpoint names?
- What components need responsive variants?
- Do you need responsive grid layouts?
- Should any elements be hidden on certain breakpoints?