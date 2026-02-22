# Tailwind Typography Prompt

## Context
User wants to configure and use the Tailwind CSS Typography plugin for styling prose content.

## Instructions
1. Install the typography plugin
2. Configure typography theme
3. Apply typography classes
4. Customize typography variants
5. Create responsive typography
6. Add custom typography styles
7. Test typography implementation

## Output
- Typography plugin installation
- Typography configuration
- Prose class usage
- Custom typography styles
- Responsive typography
- Typography examples

## Examples
Installation:
```bash
npm install @tailwindcss/typography
```

Configuration:
```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            color: '#333',
            a: {
              color: '#3b82f6',
              textDecoration: 'underline',
              fontWeight: '500',
            },
            'h1,h2,h3,h4,h5,h6': {
              fontWeight: '700',
            },
            img: {
              borderRadius: '0.5rem',
            },
          },
        },
        lg: {
          css: {
            fontSize: '1.125rem',
            lineHeight: '1.7777778',
            p: {
              marginTop: '1.3333333em',
              marginBottom: '1.3333333em',
            },
          },
        },
      },
    },
  },
}
```

Usage:
```html
<!-- Basic usage -->
<article class="prose">
  <h1>Article Title</h1>
  <p>This is a paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
  <ul>
    <li>List item 1</li>
    <li>List item 2</li>
  </ul>
</article>

<!-- Large typography -->
<article class="prose prose-lg max-w-none">
  <h1>Large Article Title</h1>
  <p>This is a larger paragraph with more readable text size.</p>
</article>

<!-- Custom colors -->
<article class="prose prose-indigo dark:prose-invert">
  <h1>Colorful Article</h1>
  <p>This article uses indigo as the primary color for links and headings.</p>
</article>
```

Custom variants:
```html
<!-- Different color schemes -->
<article class="prose prose-slate">
  <h1>Slate Prose</h1>
  <p>Using slate color palette.</p>
</article>

<article class="prose prose-neutral">
  <h1>Neutral Prose</h1>
  <p>Using neutral color palette.</p>
</article>

<!-- Size variants -->
<article class="prose prose-sm">
  <h1>Small Prose</h1>
  <p>Smaller text size.</p>
</article>

<article class="prose prose-xl">
  <h1>Extra Large Prose</h1>
  <p>Larger text size.</p>
</article>
```

Advanced customization:
```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            '--tw-prose-body': '#374151',
            '--tw-prose-headings': '#111827',
            '--tw-prose-lead': '#6b7280',
            '--tw-prose-links': '#1d4ed8',
            '--tw-prose-bold': '#111827',
            '--tw-prose-counters': '#6b7280',
            '--tw-prose-bullets': '#d1d5db',
            '--tw-prose-hr': '#e5e7eb',
            '--tw-prose-quotes': '#111827',
            '--tw-prose-quote-borders': '#e5e7eb',
            '--tw-prose-captions': '#6b7280',
            '--tw-prose-code': '#111827',
            '--tw-prose-pre-code': '#e5e7eb',
            '--tw-prose-pre-bg': 'rgb(17 24 39)',
            '--tw-prose-th-borders': '#d1d5db',
            '--tw-prose-td-borders': '#e5e7eb',
          },
        },
      },
    },
  },
}
```

Responsive typography:
```html
<!-- Responsive prose -->
<article class="prose prose-sm sm:prose-base md:prose-lg lg:prose-xl">
  <h1>Responsive Article</h1>
  <p>Text size changes based on screen size.</p>
</article>
```

Typography with custom elements:
```html
<article class="prose prose-img:rounded-xl prose-a:text-blue-600 hover:prose-a:text-blue-800">
  <h1>Custom Styled Prose</h1>
  <p>Images have rounded corners and links have custom hover states.</p>
  <img src="image.jpg" alt="Description" />
  <p>Links are <a href="#">blue by default</a> and darker on hover.</p>
</article>
```

## Questions to Ask
- What color scheme do you want for typography?
- What size variant do you need? (sm, base, lg, xl, 2xl)
- Do you need custom typography styles?
- Should typography be responsive?
- Do you need different styles for headings, paragraphs, lists?
- Are there specific fonts you want to use?