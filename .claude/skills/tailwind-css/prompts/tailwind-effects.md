# Tailwind Effects Prompt

## Context
User wants to apply visual effects using Tailwind CSS utilities and custom configurations.

## Instructions
1. Analyze effect requirements
2. Configure effect utilities
3. Create shadow variants
4. Add gradient utilities
5. Implement filter and blend effects
6. Add backdrop filters
7. Create hover effects

## Output
- Effect utility classes
- Shadow configurations
- Gradient utilities
- Filter and blend effects
- Backdrop filter variants
- Interactive effect examples

## Examples
Shadows:
```html
<!-- Box shadows -->
<div class="shadow-sm">Light shadow</div>
<div class="shadow">Regular shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
<div class="shadow-2xl">2X large shadow</div>
<div class="shadow-inner">Inner shadow</div>
<div class="shadow-none">No shadow</div>

<!-- Colored shadows -->
<div class="shadow-blue-500/50">Blue shadow</div>
<div class="shadow-purple-500/30 hover:shadow-purple-500/50 transition-shadow">
  Hover shadow
</div>

<!-- Custom shadows -->
<div class="shadow-[0_4px_6px_-1px_rgba(0,0,0,0.1)]">
  Custom shadow
</div>
```

Gradients:
```html
<!-- Background gradients -->
<div class="bg-gradient-to-r from-blue-500 to-purple-600">
  Horizontal gradient
</div>

<div class="bg-gradient-to-b from-green-400 to-blue-500">
  Vertical gradient
</div>

<div class="bg-gradient-to-tr from-pink-500 via-red-500 to-yellow-500">
  Diagonal gradient
</div>

<div class="bg-gradient-to-br from-transparent via-yellow-400 to-transparent">
  Transparent gradient
</div>

<!-- Text gradients -->
<h1 class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
  Gradient text
</h1>

<h1 class="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">
  Another gradient text
</h1>
```

Filters and blends:
```html
<!-- Filters -->
<div class="filter grayscale">
  Grayscale filter
</div>

<div class="filter sepia">
  Sepia filter
</div>

<div class="filter blur-sm">
  Blur filter
</div>

<div class="filter brightness-125">
  Brightness filter
</div>

<div class="filter contrast-150">
  Contrast filter
</div>

<div class="filter saturate-150">
  Saturation filter
</div>

<div class="filter hue-rotate-90">
  Hue rotation filter
</div>

<!-- Custom filter -->
<div class="filter drop-shadow(0_0_2px_rgba(255,255,255,0.5))">
  Custom filter
</div>
```

Backdrop filters:
```html
<div class="relative">
  <div class="bg-white/30 backdrop-blur-sm">
    Light backdrop blur
  </div>

  <div class="bg-white/20 backdrop-blur-md">
    Medium backdrop blur
  </div>

  <div class="bg-white/10 backdrop-blur-lg">
    Heavy backdrop blur
  </div>

  <div class="bg-black/30 backdrop-blur-xl backdrop-saturate-200">
    Heavy backdrop with saturation
  </div>
</div>
```

Hover effects:
```html
<!-- Scale and rotate -->
<div class="transition-transform duration-300 hover:scale-110 hover:rotate-6">
  Scale and rotate on hover
</div>

<!-- Shadow and glow -->
<div class="transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/50">
  Shadow glow on hover
</div>

<!-- Gradient shift -->
<div class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-purple-600 hover:to-blue-500 transition-all duration-300">
  Gradient shift on hover
</div>

<!-- Flip card -->
<div class="group h-64 [perspective:1000px]">
  <div class="relative h-full rounded-xl shadow-xl transition-all duration-500 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">
    <div class="absolute inset-0">
      Front content
    </div>
    <div class="absolute inset-0 [transform:rotateY(180deg)]">
      Back content
    </div>
  </div>
</div>
```

Custom effects:
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      boxShadow: {
        'glow': '0 0 20px rgba(59, 130, 246, 0.5)',
        'neon': '0 0 30px #00ffff, 0 0 60px #00ffff',
        'soft-glow': '0 0 15px rgba(255, 255, 255, 0.3)',
      },
      backgroundImage: {
        'noise': "url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDIwIEwgMjAgMCIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IxMDAlIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==')",
      },
    },
  },
}
```

## Questions to Ask
- What types of effects do you need? (shadows, gradients, filters, etc.)
- Should effects be interactive (on hover/focus)?
- Do you need backdrop filters?
- Are there any specific color requirements for effects?
- Should effects be animated or static?
- Do you need custom effect definitions?