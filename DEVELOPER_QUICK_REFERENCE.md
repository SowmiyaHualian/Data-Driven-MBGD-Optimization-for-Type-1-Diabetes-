# DiagnoSync Auth Feature - Developer Quick Reference

## 🎯 HTML Elements

### Modal IDs
```html
<div id="loginModal">...</div>
<div id="registerModal">...</div>
<div id="authSuccessModal">...</div>
```

### Form IDs
```html
<form id="login-form">...</form>
<form id="register-form">...</form>
```

### Input Field IDs
**Login Form**:
- `#login-email` - Email input
- `#login-password` - Password input
- `input[name="remember"]` - Remember me checkbox

**Register Form**:
- `#register-fname` - First name
- `#register-lname` - Last name
- `#register-email` - Email address
- `#register-password` - Password
- `#register-confirm` - Confirm password
- `input[name="terms"]` - Terms checkbox

---

## 🔧 JavaScript Functions

### Modal Control
```javascript
openLoginModal()              // Show login modal
closeLoginModal()             // Hide login modal
openRegisterModal()           // Show register modal
closeRegisterModal()          // Hide register modal
closeSuccessModal()           // Hide success modal
```

### Form Switching
```javascript
switchToRegister()            // Open register, close login
switchToLogin()               // Open login, close register
```

### Navigation
```javascript
scrollToSection('tool')       // Smooth scroll to element
scrollToSection('about')      // Scroll to about section
scrollToSection('faq')        // Scroll to FAQ section
```

---

## 🎨 CSS Classes

### Modal Classes
```css
.modal                        /* Modal backdrop */
.modal.hidden                 /* Hide modal */
.modal-content                /* Modal white box */
.modal-content-success        /* Success variant */
.modal-header                 /* Header section */
.close-modal                  /* Close button */
```

### Form Classes
```css
.auth-form                    /* Form container */
.form-group                   /* Input wrapper */
.form-row                     /* Multiple inputs in row */
.form-options                 /* Checkbox/link area */
.remember-me                  /* Remember checkbox */
.forgot-password              /* Password link */
.terms-check                  /* Terms checkbox */
```

### Button Classes
```css
.btn-login                    /* Login button (outline) */
.btn-register                 /* Register button (filled) */
.btn-primary-large            /* Submit buttons */
.btn-primary-large:hover      /* Hover state */
```

### Animation Classes (Automatic)
```css
@keyframes fadeIn             /* Modal fade-in: 300ms */
@keyframes slideUp            /* Modal slide-up: 300ms */
@keyframes scaleIn            /* Success icon: 400ms */
@keyframes float              /* Background blobs: 20s */
```

---

## 🌐 API Endpoints

### Current (Demo/Development)
```
POST /api/login
POST /api/register
```

### Request Format
```javascript
// Login
{
  "email": "user@example.com",
  "password": "password123",
  "remember": true
}

// Register
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

### Response Format
```javascript
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## 📦 Local Storage Keys

```javascript
localStorage.getItem('authToken')      // JWT token
localStorage.setItem('authToken', token)

localStorage.getItem('userEmail')      // User email
localStorage.setItem('userEmail', email)

localStorage.getItem('userName')       // Full name
localStorage.setItem('userName', name)

localStorage.getItem('apiUrl')         // API base URL
localStorage.setItem('apiUrl', url)
```

---

## 🎨 CSS Variables

```css
:root {
  --medical-blue: #0066cc;
  --medical-teal: #00a8a8;
  --medical-light: #e6f2ff;
  
  --accent-glow: #2563eb;
  --accent-glow-secondary: #06b6d4;
  
  --text-primary: #1e293b;
  --text-secondary: #475569;
  --glass-bg: rgba(255, 255, 255, 0.85);
  
  --danger: #ef4444;
  --safe: #10b981;
  --warning: #f59e0b;
}
```

---

## 📱 Responsive Breakpoints

```css
Desktop:  1200px+
Tablet:   768px - 1200px
Mobile:   < 768px
```

---

## 🔑 Key Functions Implementation

### Opening Login Modal
```javascript
function openLoginModal() {
  document.getElementById('loginModal').classList.remove('hidden');
  document.getElementById('registerModal').classList.add('hidden');
}
```

### Handling Form Submission
```javascript
document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  
  // API call
  const response = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  // Handle response...
});
```

### Storing Auth Data
```javascript
if (response.ok) {
  const data = await response.json();
  localStorage.setItem('authToken', data.token);
  localStorage.setItem('userEmail', email);
}
```

---

## 🧩 Component Hierarchy

```
<body>
  <nav class="navbar">
    <div class="nav-container">
      <div class="logo-small">...</div>
      <ul class="nav-links">
        <li><a>Assessment Tool</a></li>
        <li><a>About</a></li>
        <li><a>FAQ</a></li>
        <li class="auth-links">
          <button class="btn-login">Login</button>
          <button class="btn-register">Register</button>
        </li>
      </ul>
    </div>
  </nav>

  <div id="loginModal" class="modal">
    <div class="modal-content">
      <button class="close-modal">×</button>
      <div class="modal-header">...</div>
      <form class="auth-form" id="login-form">...</form>
    </div>
  </div>

  <div id="registerModal" class="modal">
    <!-- Similar structure -->
  </div>

  <div id="authSuccessModal" class="modal">
    <div class="modal-content modal-success">
      <div class="success-icon">✓</div>
      <h2 id="successTitle">...</h2>
      <p id="successMessage">...</p>
      <button class="btn-primary-large">...</button>
    </div>
  </div>

  <main class="container">
    <!-- Main content -->
  </main>

  <script src="app.js"></script>
</body>
```

---

## 🔍 Selector Reference

```javascript
// By ID
document.getElementById('loginModal')

// By class
document.getElementsByClassName('auth-form')
document.querySelectorAll('.modal')

// By attribute
document.querySelector('input[name="remember"]')
document.querySelector('input[name="terms"]')

// By tag
document.querySelectorAll('button')
document.querySelectorAll('input')

// Closest parent
element.closest('.modal-content')
```

---

## 🎬 Animation Timing

| Animation | Duration | Easing |
|-----------|----------|--------|
| Modal Fade | 300ms | Linear |
| Modal Slide | 300ms | ease |
| Success Icon | 400ms | ease |
| Progress Bar | 1500ms | linear |
| Button Hover | 300ms | ease |
| Blob Float | 20s | ease-in-out |

---

## 🛠️ Common Customizations

### Change Primary Color
```css
:root {
  --accent-glow: #YOUR-COLOR;
}
```

### Change Modal Width
```css
.modal-content {
  max-width: 600px; /* Change from 450px */
}
```

### Change Button Appearance
```css
.btn-login {
  background: --your-color;
  color: --your-color;
}
```

### Add Background Image
```css
.medical-bg {
  background-image: url('your-image.jpg');
}
```

---

## 🚀 Performance Tips

```javascript
// Use event delegation instead of individual listeners
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('btn-login')) {
    openLoginModal();
  }
});

// Debounce scroll events
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Use event.stopPropagation() to prevent bubbling
modal.addEventListener('click', (e) => {
  e.stopPropagation(); // Prevent closing when clicking inside
});
```

---

## 📋 File Locations

| File | Purpose |
|------|---------|
| `frontend/index.html` | HTML structure |
| `frontend/styles.css` | Styling & animations |
| `frontend/app.js` | JavaScript logic |
| `AUTH_FEATURE_GUIDE.md` | Full documentation |
| `TESTING_GUIDE.md` | Test procedures |
| `MEDICAL_BACKGROUND_SETUP.md` | Image setup |
| `IMPLEMENTATION_SUMMARY.md` | Change summary |

---

## 🔐 Security Checklist

- [ ] Passwords sent over HTTPS
- [ ] Passwords never logged/displayed
- [ ] JWT token verified on backend
- [ ] CSRF tokens implemented
- [ ] Input validation on backend
- [ ] Rate limiting on auth endpoints
- [ ] Secure password hashing (bcrypt)
- [ ] Token expiration implemented
- [ ] Refresh token mechanism
- [ ] Session timeout

---

## 🐛 Quick Debug Commands

```javascript
// Check modal visibility
document.getElementById('loginModal').classList.toggle('hidden')

// Check localStorage
Object.keys(localStorage)
localStorage.clear() // Clear all

// Force form validation
document.getElementById('login-form').checkValidity()

// Simulate form submission
document.getElementById('login-form').dispatchEvent(
  new Event('submit', { bubbles: true })
)

// Get all form values
const formData = new FormData(document.getElementById('login-form'))
Object.fromEntries(formData)
```

---

## 📞 API Test URLs

For testing with your API:
```
Login:    POST http://your-api.com/api/login
Register: POST http://your-api.com/api/register
```

Test with curl:
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

**Quick Link References**:
- WHO Design: https://www.who.int/
- Medical Images: https://unsplash.com/s/photos/medical
- MDN Docs: https://developer.mozilla.org
- CSS Tips: https://css-tricks.com

**Last Updated**: March 2026

