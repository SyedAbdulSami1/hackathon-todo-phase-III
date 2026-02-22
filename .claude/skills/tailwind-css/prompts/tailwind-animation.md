# Tailwind Animation Prompt

## Context
User wants to create and use custom animations and transitions with Tailwind CSS.

## Instructions
1. Analyze animation requirements
2. Create keyframe animations
3. Define animation utilities
4. Add transition utilities
5. Create animation variants
6. Implement performance optimizations
7. Add accessibility considerations

## Output
- Animation keyframes
- Custom animation utilities
- Transition utilities
- Animation variants
- Performance optimizations
- Accessibility notes

## Examples
Custom animations:
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-slow': 'bounce 2s infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
}
```

Animation utilities:
```html
<!-- Using custom animations -->
<div class="animate-fade-in">
  Fade in animation
</div>

<div class="animate-slide-up">
  Slide up animation
</div>

<div class="animate-bounce-slow">
  Slow bounce animation
</div>
```

Transitions:
```html
<!-- Simple transitions -->
<div class="transition-colors duration-300 hover:bg-blue-500">
  Hover to change color
</div>

<div class="transition-all duration-500 hover:scale-110">
  Hover to scale up
</div>

<div class="transition-transform duration-300 hover:rotate-12">
  Hover to rotate
</div>
```

Complex animations:
```jsx
// Animated component
const AnimatedCard = ({ isVisible }) => {
  return (
    <div className={`
      transition-all duration-500 ease-out
      transform origin-center
      ${isVisible
        ? 'opacity-100 translate-y-0 scale-100'
        : 'opacity-0 translate-y-4 scale-95'
      }
    `}>
      <div className="bg-white rounded-lg shadow-lg p-6">
        Content here
      </div>
    </div>
  )
}
```

Animation with hover effects:
```html
<div class="group relative overflow-hidden rounded-lg">
  <img src="image.jpg" alt="Description" class="transition-transform duration-300 group-hover:scale-110" />
  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 flex items-center justify-center">
    <span class="text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      View Details
    </span>
  </div>
</div>
```

Performance optimizations:
```css
/* For better performance */
.gpu-accelerated {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

.will-change-transform {
  will-change: transform;
}
```

## Questions to Ask
- What type of animations do you need? (fade, slide, bounce, spin, etc.)
- Should animations be on hover, focus, or state changes?
- What duration and easing functions should be used?
- Do you need entrance animations for elements?
- Should animations be customizable?
- Are there performance concerns to consider?