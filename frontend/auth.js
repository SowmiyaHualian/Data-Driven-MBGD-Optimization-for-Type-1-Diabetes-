// DiagnoSync Authentication Utilities
// Shared authentication functions used across all pages

/**
 * Get the authentication token from localStorage
 */
function getAuthToken() {
    return localStorage.getItem("authToken");
}

/**
 * Get the user ID from localStorage
 */
function getUserId() {
    return localStorage.getItem("userId");
}

/**
 * Get the username from localStorage
 */
function getUsername() {
    return localStorage.getItem("username");
}

/**
 * Get the full name from localStorage  
 */
function getFullName() {
    return localStorage.getItem("fullName");
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return !!getAuthToken();
}

/**
 * Require authentication and redirect to login if not authenticated
 */
function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
        return false;
    }
    return true;
}

/**
 * Logout user and clear localStorage
 */
function logout() {
    localStorage.removeItem("authToken");
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
    localStorage.removeItem("fullName");
    window.location.href = "index.html";
}

/**
 * Make an authenticated API call
 */
async function authenticatedFetch(url, options = {}) {
    const token = getAuthToken();
    
    if (!options.headers) {
        options.headers = {};
    }
    
    options.headers["Content-Type"] = "application/json";
    
    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }
    
    return fetch(url, options);
}

/**
 * Format date to readable format
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

/**
 * Get risk level class names for styling
 */
function getRiskLevelClass(riskLevel) {
    const level = riskLevel.toLowerCase();
    if (level === "high") return "risk-high";
    if (level === "moderate") return "risk-moderate";
    if (level === "low") return "risk-low";
    return "risk-low";
}

/**
 * Get risk level icon/emoji
 */
function getRiskLevelIcon(riskLevel) {
    const level = riskLevel.toLowerCase();
    if (level === "high") return "🚨";
    if (level === "moderate") return "⚠️";
    if (level === "low") return "✓";
    return "✓";
}
