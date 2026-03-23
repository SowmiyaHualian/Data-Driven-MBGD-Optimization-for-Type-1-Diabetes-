# 🧪 DiagnoSync Authentication - Quick Test Guide

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- No backend required for initial testing (demo mode)

### Local Testing
1. Open `frontend/index.html` in your browser
2. Or run a simple local server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Then visit: http://localhost:8000/frontend/
   ```

## 📋 Test Scenarios

### Test 1: Login Modal Opens/Closes ✓
**Steps**:
1. Click "Login" button in navbar
2. Verify login modal appears with smooth animation
3. Check form fields: Email, Password
4. Check "Remember me" checkbox
5. Check "Forgot password?" link
6. Click the X button or outside modal to close
7. Verify modal closes smoothly

**Expected**: 
- Modal fades in smoothly
- All form elements visible
- Close button functional
- Can close by clicking outside

---

### Test 2: Register Modal Opens/Closes ✓
**Steps**:
1. Click "Register" button in navbar
2. Verify registration modal appears
3. Check form fields: First Name, Last Name, Email, Password, Confirm Password
4. Check Terms checkbox
5. Verify password requirement text shows
6. Click close button

**Expected**:
- Modal displays with all fields
- Mobile responsiveness (if on mobile)
- Smooth animations
- Clear form validation hints

---

### Test 3: Switch Between Login & Register ✓
**Steps**:
1. Open Login modal
2. Click "Register here" link at bottom
3. Verify Register modal opens, Login closes
4. Click "Sign in" link at bottom of Register
5. Verify Login modal opens, Register closes

**Expected**:
- Seamless switching without page reload
- No data loss between switches
- Smooth transitions

---

### Test 4: Login Form Validation ✓
**Steps**:
1. Open Login modal
2. Click Submit without entering anything
3. Try entering invalid email (test@)
4. Enter valid email only, click Submit
5. Enter valid email and password, click Submit

**Expected**:
- Form requires email
- Form requires password
- Success modal appears on valid submission
- localStorage contains authToken and userEmail

---

### Test 5: Register Form Validation ✓
**Steps**:
1. Open Register modal
2. Try submitting empty form
3. Enter first name only, try submit
4. Enter all fields with mismatched passwords
5. Check error message for password mismatch
6. Enter password < 8 characters, try submit
7. Check error about password length
8. Don't check terms, try submit
9. Fill complete form correctly, submit

**Expected**:
- Form requires all fields
- Password must be 8+ characters
- Passwords must match
- Terms must be accepted
- Success modal appears on valid submission

---

### Test 6: Success Modal ✓
**Steps**:
1. Complete login or registration successfully
2. Check success modal appears with:
   - Green checkmark (✓)
   - Personalized message
   - Continue button
3. Click Continue button
4. Page smoothly scrolls to Assessment Tool section

**Expected**:
- Success modal animates in
- Message is personalized
- localStorage has user data
- Clicking Continue scrolls to tool section

---

### Test 7: Form Data in localStorage ✓
**Steps**:
1. Complete registration with:
   - Email: test@example.com
   - First Name: John
   - Last Name: Doe
2. Open browser DevTools (F12)
3. Go to Application → localStorage
4. Check for keys:
   - `authToken`: Should have a value
   - `userEmail`: Should be "test@example.com"
   - `userName`: Should be "John Doe"

**Expected**:
- All three keys present
- Values correct
- Persist after page reload

---

### Test 8: Responsive Design ✓
**Mobile (< 768px)**:
1. Resize browser to mobile width (375px)
2. Click Login/Register buttons
3. Verify modal is full width with padding
4. Check form inputs are properly sized
5. Verify buttons stack on mobile
6. Test on actual mobile device if possible

**Expected**:
- Modal takes up 95% width with max-width fallback
- Text is readable
- No overflow or cut-off content
- Touch targets are at least 44x44 pixels
- Font size is at least 16px on inputs (prevents iOS zoom)

---

### Test 9: Modal Background Click ✓
**Steps**:
1. Open any modal
2. Verify clicking the gray background (outside modal) closes it
3. Click on the white modal content
4. Verify clicking content doesn't close modal

**Expected**:
- Clicking outside modal closes it
- Clicking inside modal keeps it open
- Works for all modals (Login, Register, Success)

---

### Test 10: Smooth Animations ✓
**Steps**:
1. Observe modal entrance (fade + slide up)
2. Click buttons and observe hover effects (lift effect)
3. Watch success icon scale animation
4. Observe progress bar animation during assessment

**Expected**:
- All animations smooth (60 FPS)
- No jank or stuttering
- Hover effects responsive
- Transitions use 300ms for modals, 1500ms for progress

---

### Test 11: Navigation Functions ✓
**Steps**:
1. Click "Assessment Tool" in navbar
2. Page smoothly scrolls to that section
3. Click "About" - scrolls to that section
4. Click "FAQ" - scrolls to that section

**Expected**:
- Smooth scroll behavior
- All sections accessible
- Navbar links work during all states

---

### Test 12: Error Handling (Demo Mode) ✓
**Steps**:
1. With no backend running
2. Submit login/register form
3. Should still work (demo fallback)
4. Check localStorage for token

**Expected**:
- No console errors
- Demo mode activates automatically
- Form submits successfully with mock token
- Success modal appears

---

## 🎨 Visual Inspection Checklist

- [ ] Colors are professional medical blues/teals
- [ ] Text is readable over background
- [ ] Buttons have clear hover effects
- [ ] Forms have proper spacing and alignment
- [ ] Icons/checkmarks render correctly
- [ ] No text overflow in any field
- [ ] Gradient background displays smoothly
- [ ] Modal shadows look professional

---

## ♿ Accessibility Checks

- [ ] Can tab through all form fields
- [ ] All inputs have associated labels
- [ ] Color not the only indicator (✓ icon visible)
- [ ] Buttons have visible focus state
- [ ] Success message is clear text (not just visual)
- [ ] Font sizes are readable (14px+ for body)
- [ ] Contrast ratio is sufficient (4.5:1 for normal text)

---

## 🐛 Debugging Tips

### Check Browser Console
```javascript
// In browser console:
localStorage.getItem('authToken')     // Check token
localStorage.getItem('userEmail')     // Check email
document.getElementById('loginModal')  // Check element exists
```

### Test Modal Functions
```javascript
// In browser console, test functions directly:
openLoginModal()          // Should open login
closeLoginModal()         // Should close login
openRegisterModal()       // Should open register
scrollToSection('tool')   // Should scroll
```

### Network Tab
- Open DevTools → Network tab
- Submit login/register form
- If backend is connected, see `/api/login` or `/api/register` request
- Check response headers and body
- No request = Demo mode (expected without backend)

### Performance
- Open DevTools → Performance
- Record while opening/closing modals
- Check for smooth 60 FPS
- Look for any long tasks (>50ms)

---

## 🔄 Integration Testing (With Backend)

### When Your Backend is Ready:

1. **Update API Endpoints** in `app.js`:
   - Find `/api/login`
   - Find `/api/register`
   - Ensure your backend is running

2. **Test Login Flow**:
   ```
   Test account: test@example.com / password123
   Backend receives: POST /api/login
   Should return: { "token": "jwt-token-here" }
   Token stored in: localStorage.authToken
   ```

3. **Test Register Flow**:
   ```
   New account data sent to: POST /api/register
   Backend creates user account
   Should return: { "token": "jwt-token-here" }
   ```

4. **Verify Data Persistence**:
   - Close and reopen page
   - Check if user still logged in
   - Verify token still in localStorage

---

## 📊 Test Results Template

```
Test Case: ________________
Date: _______ / _______ / _______
Browser: ________________________
Device: __________________________

✓ PASS  / ✗ FAIL / ⚠ PARTIAL

Notes:
_________________________________
_________________________________

Expected Result:
_________________________________

Actual Result:
_________________________________
```

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Modal not appearing | Check console for errors, verify IDs match |
| Form not submitting | Check email format, ensure all fields filled |
| localStorage empty | Check if browser allows storage, try incognito |
| Animations jerky | Check GPU acceleration, reduce other processes |
| Text overlapping | Check font size in CSS, verify responsive design |
| Mobile layout broken | Test at actual mobile dimensions (375x667) |
| Button not clickable | Check z-index, verify no overlay elements |
| Close button doesn't work | Verify onclick handler, check HTML id attribute |

---

## ✅ Pre-Launch Checklist

- [ ] All tests pass on desktop (Chrome, Firefox, Safari, Edge)
- [ ] All tests pass on mobile (iOS Safari, Chrome Mobile)
- [ ] localStorage persists correctly
- [ ] No console errors or warnings
- [ ] Animations smooth at 60 FPS
- [ ] Responsive design works at all breakpoints
- [ ] Accessibility requirements met
- [ ] Backend integration verified (if applicable)
- [ ] Documentation reviewed
- [ ] User feedback collected

---

## 📚 Additional Resources

- **MDN Web Docs**: https://developer.mozilla.org
- **Can I Use**: https://caniuse.com (browser compatibility)
- **WCAG Accessibility**: https://www.w3.org/WAI/WCAG21/quickref/
- **CSS Tricks**: https://css-tricks.com/ (animations, responsive design)

---

**Remember**: These tests should all pass before deploying to production. If any test fails, refer to the troubleshooting guide or check the documentation files.

**Good luck testing!** 🎉

