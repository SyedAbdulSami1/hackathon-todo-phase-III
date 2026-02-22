# Card Component Example

This example demonstrates a versatile card component using Tailwind CSS, incorporating multiple skills:

- **tailwind-components** for reusable card structure
- **tailwind-effects** for visual enhancements
- **tailwind-responsive** for responsive behavior
- **tailwind-dark-mode** for dark mode support
- **tailwind-animation** for subtle interactions

## HTML Implementation

```html
<!-- Basic Card -->
<div class="max-w-sm rounded-xl overflow-hidden shadow-lg bg-white dark:bg-gray-800 transition-all duration-300 hover:shadow-xl">
  <img class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80" alt="Profile picture">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2 text-gray-800 dark:text-white">John Doe</div>
    <p class="text-gray-700 dark:text-gray-300 text-base">
      Software Engineer passionate about creating beautiful and functional user experiences.
    </p>
  </div>
  <div class="px-6 pt-4 pb-2">
    <span class="inline-block bg-gray-200 dark:bg-gray-700 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 dark:text-gray-300 mr-2 mb-2">#developer</span>
    <span class="inline-block bg-gray-200 dark:bg-gray-700 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 dark:text-gray-300 mr-2 mb-2">#ui/ux</span>
    <span class="inline-block bg-gray-200 dark:bg-gray-700 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 dark:text-gray-300 mr-2 mb-2">#webdev</span>
  </div>
</div>

<!-- Feature Card -->
<div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 max-w-md">
  <div class="flex items-center mb-4">
    <div class="bg-indigo-100 dark:bg-indigo-900/30 p-3 rounded-lg mr-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      </svg>
    </div>
    <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Secure Storage</h3>
  </div>
  <p class="text-gray-600 dark:text-gray-300 mb-4">
    Your data is encrypted and securely stored with enterprise-grade security measures.
  </p>
  <button class="mt-2 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-300">
    Learn More
  </button>
</div>

<!-- Pricing Card -->
<div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden max-w-sm">
  <div class="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
    <h3 class="text-2xl font-bold">Premium Plan</h3>
    <div class="mt-4">
      <span class="text-4xl font-extrabold">$29</span>
      <span class="text-indigo-200">/month</span>
    </div>
  </div>
  <div class="p-6">
    <ul class="space-y-4 mb-6">
      <li class="flex items-center">
        <svg class="h-5 w-5 text-green-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <span class="text-gray-700 dark:text-gray-300">Unlimited projects</span>
      </li>
      <li class="flex items-center">
        <svg class="h-5 w-5 text-green-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <span class="text-gray-700 dark:text-gray-300">Priority support</span>
      </li>
      <li class="flex items-center">
        <svg class="h-5 w-5 text-green-500 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <span class="text-gray-700 dark:text-gray-300">Advanced analytics</span>
      </li>
    </ul>
    <button class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-300">
      Get Started
    </button>
  </div>
</div>

<!-- Blog Card -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 max-w-md">
  <img class="w-full h-48 object-cover" src="https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80" alt="Blog post image">
  <div class="p-6">
    <div class="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-2">
      <time datetime="2023-01-01">Jan 1, 2023</time>
      <span class="mx-2">•</span>
      <span>5 min read</span>
    </div>
    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">The Future of Web Development</h3>
    <p class="text-gray-600 dark:text-gray-300 mb-4">
      Exploring the latest trends and technologies shaping the future of web development...
    </p>
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <img class="w-10 h-10 rounded-full mr-3" src="https://randomuser.me/api/portraits/men/32.jpg" alt="Author">
        <div>
          <p class="text-sm font-medium text-gray-900 dark:text-white">Alex Johnson</p>
          <p class="text-xs text-gray-500 dark:text-gray-400">Senior Developer</p>
        </div>
      </div>
      <button class="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium text-sm">
        Read more →
      </button>
    </div>
  </div>
</div>
```

## Key Features Demonstrated

1. **Component Structure**:
   - Reusable card component with header, content, and footer sections
   - Consistent padding and spacing with Tailwind utilities
   - Flexible layout that works for different content types

2. **Visual Effects**:
   - Subtle shadows for depth perception
   - Rounded corners for modern appearance
   - Gradient backgrounds for visual interest
   - Hover effects for interactivity

3. **Responsive Design**:
   - Fixed maximum width for consistent sizing
   - Flexible padding that adapts to screen size
   - Properly sized images that maintain aspect ratio

4. **Dark Mode Support**:
   - Different background colors for dark mode
   - Appropriate text colors for contrast
   - Consistent styling across light and dark themes

5. **Interactive Elements**:
   - Hover effects on cards and buttons
   - Smooth transitions for state changes
   - Visual feedback for user interactions

6. **Typography**:
   - Clear hierarchy with font weights and sizes
   - Appropriate line heights for readability
   - Consistent text styling across elements

This example showcases how to create versatile card components that can be adapted for different use cases while maintaining a consistent design language and responsive behavior.