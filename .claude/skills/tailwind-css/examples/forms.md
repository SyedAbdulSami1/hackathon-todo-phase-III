# Form Component Example

This example demonstrates a comprehensive form component using Tailwind CSS, incorporating multiple skills:

- **tailwind-forms** for form styling
- **tailwind-states** for interactive states
- **tailwind-effects** for visual feedback
- **tailwind-dark-mode** for dark mode support
- **tailwind-responsive** for responsive behavior

## HTML Implementation

```html
<!-- Contact Form -->
<div class="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
  <h2 class="text-2xl font-bold text-gray-800 dark:text-white mb-6">Contact Us</h2>
  <form class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="first-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">First Name</label>
        <input type="text" id="first-name" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors">
      </div>
      <div>
        <label for="last-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Name</label>
        <input type="text" id="last-name" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors">
      </div>
    </div>

    <div>
      <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Address</label>
      <input type="email" id="email" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors" placeholder="you@example.com">
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">We'll never share your email with anyone else.</p>
    </div>

    <div>
      <label for="company" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company</label>
      <input type="text" id="company" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors">
    </div>

    <div>
      <label for="subject" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Subject</label>
      <select id="subject" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors">
        <option>Select an option</option>
        <option>General Inquiry</option>
        <option>Support Request</option>
        <option>Feature Request</option>
        <option>Bug Report</option>
      </select>
    </div>

    <div>
      <label for="message" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Message</label>
      <textarea id="message" rows="4" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors"></textarea>
    </div>

    <div class="flex items-start">
      <div class="flex items-center h-5">
        <input id="terms" type="checkbox" class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 dark:focus:ring-indigo-400 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600">
      </div>
      <div class="ml-3 text-sm">
        <label for="terms" class="font-medium text-gray-700 dark:text-gray-300">I agree to the Terms and Conditions</label>
        <p class="text-gray-500 dark:text-gray-400">By submitting this form, you consent to our privacy policy.</p>
      </div>
    </div>

    <div>
      <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 dark:focus:ring-indigo-400">
        Send Message
      </button>
    </div>
  </form>
</div>

<!-- Login Form -->
<div class="max-w-md mx-auto bg-white dark:bg-gray-800 shadow-xl rounded-lg overflow-hidden">
  <div class="p-8">
    <div class="text-center">
      <h2 class="text-3xl font-bold text-gray-800 dark:text-white">Sign in to your account</h2>
      <p class="mt-2 text-gray-600 dark:text-gray-300">Or <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">create a new account</a></p>
    </div>

    <form class="mt-8 space-y-6">
      <div>
        <label for="login-email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email address</label>
        <input type="email" id="login-email" class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors" placeholder="you@example.com">
      </div>

      <div>
        <div class="flex items-center justify-between mb-1">
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
          <a href="#" class="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">Forgot password?</a>
        </div>
        <input type="password" id="password" class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:focus:ring-indigo-400 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors" placeholder="••••••••">
      </div>

      <div class="flex items-center">
        <input id="remember-me" type="checkbox" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded dark:bg-gray-700 dark:border-gray-600">
        <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">Remember me</label>
      </div>

      <div>
        <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 dark:focus:ring-indigo-400">
          Sign in
        </button>
      </div>
    </form>

    <div class="mt-6">
      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">Or continue with</span>
        </div>
      </div>

      <div class="mt-6 grid grid-cols-3 gap-3">
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
        </button>
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M22.675 0h-21.35c-.732 0-1.325.593-1.325 1.325v21.351c0 .731.593 1.324 1.325 1.324h11.495v-9.294h-3.128v-3.622h3.128v-2.671c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12v9.293h6.116c.73 0 1.323-.593 1.323-1.325v-21.35c0-.732-.593-1.325-1.325-1.325z"/></svg>
        </button>
        <button class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z"/></svg>
        </button>
      </div>
    </div>
  </div>
</div>

<!-- Form Validation Example -->
<div class="max-w-md mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
  <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Form with Validation States</h3>

  <div class="mb-4">
    <label for="valid-field" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Valid Field</label>
    <input type="text" id="valid-field" class="w-full px-4 py-2 border border-green-500 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors" value="Valid input">
    <p class="mt-1 text-sm text-green-600 dark:text-green-400">This field is valid!</p>
  </div>

  <div class="mb-4">
    <label for="invalid-field" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Invalid Field</label>
    <input type="text" id="invalid-field" class="w-full px-4 py-2 border border-red-500 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors" value="Invalid input">
    <p class="mt-1 text-sm text-red-600 dark:text-red-400">This field has an error!</p>
  </div>

  <div class="mb-4">
    <label for="disabled-field" class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Disabled Field</label>
    <input type="text" id="disabled-field" class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed" value="Disabled input" disabled>
  </div>

  <div class="mb-4">
    <label for="loading-field" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Loading State</label>
    <div class="relative">
      <input type="text" id="loading-field" class="w-full px-4 py-2 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-colors" value="Processing...">
      <div class="absolute inset-y-0 right-0 flex items-center pr-3">
        <svg class="animate-spin h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    </div>
  </div>
</div>
```

## Key Features Demonstrated

1. **Form Structure**:
   - Proper semantic HTML for forms
   - Consistent layout with grid and flexbox
   - Logical grouping of related elements

2. **Input Styling**:
   - Consistent styling for all input types
   - Focus states with ring indicators
   - Placeholder text styling
   - Disabled and readonly states

3. **Validation States**:
   - Success state with green border
   - Error state with red border
   - Helper text for validation messages
   - Loading state with spinner

4. **Interactive Elements**:
   - Hover and focus states for all interactive elements
   - Smooth transitions between states
   - Proper focus management for accessibility

5. **Responsive Design**:
   - Grid layouts that adapt to screen size
   - Appropriate spacing on all devices
   - Mobile-first approach with desktop enhancements

6. **Dark Mode Support**:
   - Different colors for dark theme
   - Consistent styling across themes
   - Appropriate contrast ratios

7. **Visual Feedback**:
   - Clear indication of interactive elements
   - Visual cues for required fields
   - Loading indicators for processing states

This example showcases how to create comprehensive form components that provide excellent user experience with proper validation, accessibility, and responsive design.