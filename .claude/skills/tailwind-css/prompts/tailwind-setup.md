# Tailwind CSS Setup Prompt

## Context
User wants to initialize Tailwind CSS in a project. This is the first step in using Tailwind.

## Instructions
1. First, detect the project type (ask if not clear)
2. Check if Tailwind is already installed
3. Install Tailwind via npm/yarn
4. Create/update the main CSS file
5. Configure Tailwind CSS
6. Update the build process
7. Verify the setup

## Output
- Installation commands
- CSS file content
- Tailwind config file
- Build configuration updates
- Verification steps

## Examples
For Next.js:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

For Create React App:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

For plain HTML:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Questions to Ask
- What type of project is this? (Next.js, React, Vue, plain HTML, etc.)
- Where should the CSS file be located?
- Are there any specific CSS frameworks already in use?
- Do you want to include any specific plugins by default?