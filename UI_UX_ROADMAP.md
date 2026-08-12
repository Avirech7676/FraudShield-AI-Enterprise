# UI_UX_ROADMAP.md — 2026 Enterprise FinTech Design System & UI/UX Strategy

## 1. Design Vision & Aesthetic Direction

### A. Core Philosophy
FraudShield AI Enterprise is a high-stakes, real-time security & threat intelligence platform. The design system must inspire **trust**, **precision**, **speed**, and **clarity**.

- **Modern 2026 FinTech Aesthetic**: Clean dark-first theme with full light mode support. Tactile depth, crisp typography, micro-glows on high-risk alerts, subtle glassmorphism (layered frosted surfaces with sub-pixel borders), and dynamic visual data representations.
- **Human-Designed Feel**: Purposeful spacing (4px/8px modular grid), distinct visual hierarchy, zero visual noise or generic template layouts.
- **Accessibility & Ergonomics**: Built to WCAG 2.1 AA standards with high-contrast text, clear focus rings, keyboard navigation, and motion-reduced options.

---

## 2. Color System & Design Tokens

### A. CSS Custom Properties Framework (`[data-theme="dark"]` & `[data-theme="light"]`)

```css
/* Dark Theme (Default) */
[data-theme="dark"] {
  --bg-app: #090D16;
  --bg-surface: #0F172A;
  --bg-card: #1E293B;
  --bg-glass: rgba(15, 23, 42, 0.75);
  
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-medium: rgba(255, 255, 255, 0.15);
  --border-accent: rgba(99, 102, 241, 0.4);
  
  --text-primary: #F8FAFC;
  --text-secondary: #94A3B8;
  --text-muted: #64748B;
  
  --accent-primary: #6366F1;
  --accent-hover: #4F46E5;
  --accent-glow: rgba(99, 102, 241, 0.25);
  
  --risk-critical: #EF4444;
  --risk-critical-bg: rgba(239, 68, 68, 0.15);
  --risk-high: #F97316;
  --risk-high-bg: rgba(249, 115, 22, 0.15);
  --risk-medium: #FBBF24;
  --risk-medium-bg: rgba(251, 191, 36, 0.15);
  --risk-low: #10B981;
  --risk-low-bg: rgba(16, 185, 129, 0.15);
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 10px 30px -5px rgba(0, 0, 0, 0.7);
}

/* Light Theme */
[data-theme="light"] {
  --bg-app: #F8FAFC;
  --bg-surface: #FFFFFF;
  --bg-card: #F1F5F9;
  --bg-glass: rgba(255, 255, 255, 0.85);
  
  --border-subtle: #E2E8F0;
  --border-medium: #CBD5E1;
  --border-accent: rgba(79, 70, 229, 0.3);
  
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-muted: #94A3B8;
  
  --accent-primary: #4F46E5;
  --accent-hover: #4338CA;
  --accent-glow: rgba(79, 70, 229, 0.15);
  
  --risk-critical: #DC2626;
  --risk-critical-bg: #FEE2E2;
  --risk-high: #EA580C;
  --risk-high-bg: #FFEDD5;
  --risk-medium: #D97706;
  --risk-medium-bg: #FEF3C7;
  --risk-low: #059669;
  --risk-low-bg: #D1FAE5;
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 25px -5px rgba(15, 23, 42, 0.1);
}
```

---

## 3. Typography Scale

- **Primary Font**: `Inter`, system-ui, -apple-system, sans-serif
- **Monospace Font**: `JetBrains Mono`, `Fira Code`, monospace

| Class / Token | Size | Weight | Line Height | Letter Spacing | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `text-display` | 32px (2rem) | 700 (Bold) | 1.2 | -0.025em | Main dashboard headlines |
| `text-h1` | 24px (1.5rem) | 600 (SemiBold) | 1.3 | -0.02em | Page headers |
| `text-h2` | 20px (1.25rem) | 600 (SemiBold) | 1.4 | -0.01em | Card section titles |
| `text-h3` | 16px (1rem) | 600 (SemiBold) | 1.5 | 0 | Subheadings & table headers |
| `text-body` | 14px (0.875rem) | 400 (Regular) | 1.5 | 0 | Standard UI text, labels, inputs |
| `text-small` | 12px (0.75rem) | 500 (Medium) | 1.4 | 0.01em | Captions, timestamps, tooltips |
| `text-mono` | 13px (0.8125rem)| 500 (Medium) | 1.4 | 0 | Transaction IDs, JSON, hashes |

---

## 4. Reusable Design System Component Specification

### A. Buttons & Controls
1. **Primary Button**: Accent background with hover brightness scale and active scale (0.98).
2. **Secondary Button**: Outlined border with subtle background fill on hover.
3. **Danger Button**: Crimson red fill for destructive actions (Delete case, terminate stream).
4. **Ghost / Icon Button**: Minimalist background, focus ring, tooltip integration.
5. **Loading States**: Integrated spinner icon, disabled interaction state.

### B. Inputs & Filters
1. **Text & Number Input**: Sub-pixel border, floating/top labels, focus ring (`var(--accent-primary)`), clear error messaging.
2. **Select Dropdown**: Custom accessible popover menu with keyboard navigation (Up/Down/Enter/Esc).
3. **Search Bar**: Built-in search icon (`Ctrl+K` shortcut indicator), clear button (`×`).
4. **Filter Pills**: Interactive multi-select tags for Risk Level, Status, Date Range.

### C. Cards & Containers
1. **Glass Card**: `background: var(--bg-glass)`, `backdrop-filter: blur(12px)`, `border: 1px solid var(--border-subtle)`.
2. **Interactive Metric Card**: Hover translation (`translateY(-2px)`), glow shadow on focus/hover, mini trend indicator (+12.4%).
3. **Accordion Container**: Smooth height transition for SHAP feature details & rule engine breakdowns.

### D. Tables & Data Grids
1. **Header Row**: Sticky positioning, subtle border-bottom, uppercase small bold text.
2. **Row Hover & Selection**: Highlight row background on hover, checkbox selection support, double-click to view details.
3. **Pagination Bar**: Rows-per-page selector, total count display, previous/next page buttons.

### E. Dialogs, Modals & Drawer Overlays
1. **Modal Container**: Centered dialog with frosted backdrop overlay, exit cross button, Esc key listener, focus lock.
2. **Drawer Panel**: Slide-in right panel for quick Transaction Details & SHAP Explanations without leaving current view.

### F. Data Visualization & Charts
1. **Custom Recharts Styling**: Unified tooltip with dark frosted glass container, rounded corners, custom legend items.
2. **Chart Types**:
   - Area Charts for stream volume & fraud probability over time.
   - Bar Charts for risk level distributions and model metric comparisons.
   - Waterfall / Horizontal Bar Charts for SHAP feature contributions (+/- impact).

### G. Status Badges & Loading States
1. **Risk Score Pill**:
   - High Risk (>0.70): Crimson badge with dynamic pulsing dot.
   - Medium Risk (0.30–0.70): Amber badge.
   - Low Risk (<0.30): Emerald green badge.
2. **Skeletons**: Shimmer effect for metric cards, chart loaders, and table rows.
3. **Empty States**: Icon illustration, clear descriptive text, primary call-to-action button.

### H. Navigation & Shell Layout
1. **Collapsible Sidebar**:
   - Brand logo with gradient icon.
   - Navigation links with active indicator bar and badge counters (e.g. pending alerts count).
   - Tooltip support when collapsed.
2. **Topbar**:
   - Global search input (`Ctrl + K`).
   - Real-time backend status pulse indicator ("Live Engine Active").
   - Theme Switcher toggle (Sun / Moon icon).
   - User profile menu with Role tag (Admin / Analyst).

---

## 5. Accessibility & Interaction Guidelines

- **Contrast Ratios**: Body text strictly >= 4.5:1 against background in both Dark and Light modes.
- **Focus Rings**: `outline: 2px solid var(--accent-primary)`, `outline-offset: 2px` on all focusable elements.
- **Keyboard Navigation**: Full support for `Tab`, `Shift+Tab`, `Space`, `Enter`, `Escape`, arrow keys in dropdowns/modals.
- **Screen Readers**: `aria-label`, `aria-expanded`, `aria-selected`, `role="dialog"`, `role="status"`.

---

## 6. Implementation Plan (Phases 3 & 4 Blueprint)

### Phase 3: Design System Core (`src/components/ui/`)
- Setup Theme Context (`ThemeContext.tsx`) & CSS Variables (`ModernTheme.css`).
- Build basic UI building blocks: `Button`, `Input`, `Select`, `Card`, `Badge`, `Modal`, `Table`, `Skeleton`, `Dropdown`, `Toast`.
- Build navigation shell: `Sidebar`, `Header`, `ModernLayout`.

### Phase 4: Sequential Page Migration Order
1. **Login & Register**: Polished auth card, dark/light theme toggle, clear validation feedback.
2. **Dashboard**: High-impact metrics grid, real-time activity ticker, risk distribution charts.
3. **Prediction**: Single and batch fraud evaluation interface with interactive form controls.
4. **Analytics**: Deep metrics, time-series fraud trend charts, feature importance summary.
5. **Reports**: AI report generation configuration, status indicator, downloadable executive PDFs/Markdowns.
6. **Cases**: Case table, detail drawer, status assignment controls.
7. **Alerts**: Real-time alert list with quick action toggles.
8. **History**: Filterable transaction log table with multi-parameter search.
9. **Users**: User role management grid for Admins.
10. **Settings**: System configuration, threshold sliders, cache clear controls.
11. **Model Management**: Model registry table, deployment actions, performance metrics.

---

## 7. Next Steps & Approval Request

With **Phase 2 (UI/UX Strategy & Roadmap)** completed:
- Ready to proceed to **Phase 3**: Constructing the Design System architecture and reusable UI components in code without altering pages yet.
