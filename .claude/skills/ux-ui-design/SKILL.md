---
name: UX and UI Design for All Devices
description: This skill should be used when the user asks to "design responsive UI", "create cross-platform UX", "implement mobile-first design", "design for desktop, tablet, and mobile", "create adaptive layouts", "implement accessibility standards", "design inclusive interfaces", "create device-specific UI patterns", "implement responsive typography", "design for various screen sizes", "create touch-friendly interfaces", "implement accessibility features", "design for different input methods", "create cross-device experiences", or mentions UX design, UI design, responsive design, mobile design, accessibility, or cross-platform interfaces.
version: 1.0.0
---

# UX and UI Design for All Devices

This skill provides comprehensive guidance for designing user experiences and interfaces that work seamlessly across all device types and screen sizes.

## Core Principles

### Responsive Design Fundamentals
- Mobile-first approach: Start with smallest screens and progressively enhance
- Flexible grids: Use relative units (%, em, rem, vw, vh) instead of fixed pixels
- Media queries: Target specific screen sizes and device characteristics
- Flexible images: Ensure images scale appropriately across devices

### Cross-Device Consistency
- Maintain consistent branding and interaction patterns
- Preserve core functionality across all platforms
- Adapt navigation patterns to device conventions
- Consider performance implications on different hardware

## Device Categories & Specifications

### Mobile Devices
- Screen sizes: 320px - 767px
- Touch targets: Minimum 44px x 44px (iOS) or 48px x 48px (Android)
- Orientation: Portrait and landscape considerations
- Input: Touch, voice, gesture controls
- Performance: Limited processing power, battery considerations

### Tablet Devices
- Screen sizes: 768px - 1023px
- Touch targets: Minimum 44px x 44px
- Input: Touch, stylus, limited keyboard support
- Layout: Multi-panel interfaces, split views possible
- Context: Media consumption, productivity tasks

### Desktop/Laptop
- Screen sizes: 1024px+ (varies widely)
- Input: Mouse, keyboard, trackpad
- Interaction: Hover states, precise cursor control
- Layout: Complex multi-column layouts
- Performance: Higher processing power available

### Large Screens (Desktop Monitors, TVs)
- Screen sizes: 1200px+ (up to 4K and beyond)
- Layout: Grid-based, information-dense designs
- Interaction: Keyboard shortcuts, navigation efficiency
- Accessibility: High contrast, scalable text options

## Design Framework

### Breakpoint Strategy
```css
/* Mobile-first breakpoints */
/* Small devices (mobile) */
@media (min-width: 320px) { /* styles */ }

/* Medium devices (tablets) */
@media (min-width: 768px) { /* styles */ }

/* Large devices (desktops) */
@media (min-width: 1024px) { /* styles */ }

/* Extra large devices */
@media (min-width: 1200px) { /* styles */ }
```

### Typography Scaling
- Base font size: 16px on mobile, scaling up to 18-20px on desktop
- Line height: 1.4-1.6 for body text, 1.2-1.4 for headings
- Font scaling: Use clamp() for fluid typography
```css
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem); /* scales between min and max */
}
```

### Navigation Patterns
- **Mobile**: Hamburger menu, bottom navigation, tab bars
- **Tablet**: Side navigation, collapsible menus
- **Desktop**: Horizontal navigation, mega menus, flyouts
- **Touch-friendly**: Adequate spacing, large tap targets

## Accessibility Standards

### WCAG 2.1 Compliance
- Color contrast: Minimum 4.5:1 for normal text, 3:1 for large text
- Keyboard navigation: Full functionality without mouse
- Screen reader compatibility: Proper semantic markup
- Alternative text: Descriptive alt attributes for images
- Focus indicators: Visible focus states for interactive elements

### ARIA Implementation
```html
<!-- Navigation landmark -->
<nav aria-label="Main navigation">
  <!-- Navigation items -->
</nav>

<!-- Button with accessible name -->
<button aria-label="Close dialog">✕</button>

<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  <!-- Updates announced to screen readers -->
</div>
```

## Component Design Patterns

### Cards
```html
<article class="card" role="article">
  <header class="card-header">
    <h2 class="card-title">Card Title</h2>
  </header>
  <div class="card-content">
    <p>Card content that adapts to screen size</p>
  </div>
  <footer class="card-actions">
    <button class="btn btn-primary">Action</button>
  </footer>
</article>
```

### Forms
- Label positioning: Above fields on mobile, left-aligned on desktop
- Input sizing: Full width on mobile, constrained width on desktop
- Error messaging: Inline validation, clear error indicators
- Touch targets: Adequate size for finger taps

### Buttons
- Minimum touch target: 44px x 44px
- Visual feedback: Press states, loading indicators
- Size hierarchy: Primary buttons larger than secondary
- Icon buttons: Include text labels when space permits

## Platform-Specific Guidelines

### iOS Design
- Safe areas: Account for notches, home indicators
- System fonts: Use SF Pro Display/Text
- Haptic feedback: Consider for important interactions
- Navigation: Tab bar at bottom, navigation bar at top

### Android Design
- Material Design principles: Elevation, motion, color
- System fonts: Roboto or product family
- Touch targets: 48dp minimum
- Navigation: Bottom navigation, hamburger menu

### Web Standards
- Progressive Enhancement: Core functionality without JavaScript
- Performance: Optimize for slow connections
- Browser compatibility: Support major browsers
- SEO considerations: Semantic markup, crawlable content

## Touch Interface Design

### Gesture Recognition
- Swipe: Navigate between items, dismiss content
- Pinch: Zoom in/out
- Tap: Select/click
- Long press: Contextual menus
- Double tap: Zoom or like functionality

### Touch Target Optimization
- Minimum size: 44px x 44px touch area
- Adequate spacing: 8px between adjacent targets
- Visual feedback: Press states, haptic feedback
- Error prevention: Undo options for destructive actions

## Performance Considerations

### Loading States
- Skeleton screens: Show content structure while loading
- Progress indicators: Clear feedback for ongoing processes
- Optimistic updates: Update UI before server confirmation
- Lazy loading: Load content as needed

### Animation Guidelines
- Duration: 200-500ms for most animations
- Easing: Natural acceleration/deceleration curves
- Performance: Use transform and opacity for smooth animations
- Accessibility: Respects reduced motion preferences

## Testing Across Devices

### Device Testing Strategy
- Emulation: Browser developer tools, device simulators
- Real devices: Test on actual hardware
- User testing: Observe real user interactions
- Performance monitoring: Track load times, responsiveness

### Key Metrics
- Page load time: Under 3 seconds on 3G networks
- Time to interactive: Functional within 5 seconds
- Cumulative Layout Shift: Under 0.1
- First Contentful Paint: Within 1.8 seconds

## Design Systems Approach

### Component Libraries
- Reusable components: Buttons, cards, forms, modals
- Design tokens: Consistent spacing, colors, typography
- Documentation: Clear usage guidelines
- Version control: Manage component evolution

### Style Guides
- Color palettes: Primary, secondary, accent colors
- Typography scales: Headings, body text, captions
- Spacing systems: Consistent padding, margins
- Iconography: Consistent style and sizing

## Emerging Technologies

### Foldable Devices
- Dual-screen layouts: Adapt to split-screen scenarios
- Continuity: Seamless experience across fold
- Content adaptation: Adjust for different aspect ratios

### Voice Interfaces
- Voice-first design: Consider voice as primary input
- Audio feedback: Confirmations, error states
- Conversational flows: Natural language interactions

### AR/VR Considerations
- Spatial interfaces: 3D interaction patterns
- Comfort zones: Avoid uncomfortable viewing angles
- Motion sickness: Minimize disorienting movements

## Implementation Checklist

### Pre-Launch Verification
- [ ] Responsive layout works on all target devices
- [ ] Touch targets meet minimum size requirements
- [ ] Color contrast meets accessibility standards
- [ ] Keyboard navigation is fully functional
- [ ] Screen reader compatibility tested
- [ ] Performance metrics meet requirements
- [ ] Cross-browser compatibility verified
- [ ] Form inputs work on all device types
- [ ] Images are optimized for different densities
- [ ] Animations respect user preferences

### Quality Assurance
- [ ] Content remains readable at zoom levels
- [ ] Navigation is intuitive on each platform
- [ ] Loading states provide adequate feedback
- [ ] Error messages are clear and helpful
- [ ] Interactive elements have proper affordances
- [ ] Layout maintains hierarchy across devices
- [ ] Icons are legible at all sizes
- [ ] Hover states only on appropriate devices
- [ ] Touch gestures work reliably
- [ ] Text remains readable during resize

## Best Practices Summary

1. **Start Mobile-First**: Design for smallest screens first
2. **Progressive Enhancement**: Core functionality without JavaScript
3. **Accessibility First**: Meet WCAG standards from the beginning
4. **Performance Priority**: Optimize for slow connections and devices
5. **Cross-Platform Consistency**: Maintain brand and experience consistency
6. **User-Centric Design**: Test with real users on real devices
7. **Iterative Improvement**: Continuously refine based on usage data
8. **Future-Proof**: Design for unknown future devices
9. **Content Priority**: Ensure content remains accessible regardless of device
10. **Technical Feasibility**: Balance design ambition with implementation reality