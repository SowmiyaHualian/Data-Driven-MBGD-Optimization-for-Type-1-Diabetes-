// DiagnoSync - Shared utilities
// This file is called in pages that need authentication middleware

function getAuthToken() {
    return localStorage.getItem("authToken");
}

function getUserId() {
    return localStorage.getItem("userId");
}

function getUsername() {
    return localStorage.getItem("username");
}

function getFullName() {
    return localStorage.getItem("fullName");
}

function isLoggedIn() {
    return !!getAuthToken();
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = "/frontend/login.html";
        return false;
    }
    return true;
}

function logout() {
    localStorage.removeItem("authToken");
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
    localStorage.removeItem("fullName");
    window.location.href = "/frontend/login.html";
}

// API endpoints
const API_BASE = window.location.origin + "/api";
const API_LOGIN = API_BASE + "/login";
const API_REGISTER = API_BASE + "/register";
const API_PREDICT = API_BASE + "/predict";
const API_PROFILE = API_BASE + "/user/profile";

// Make API calls with authentication
async function authenticatedFetch(url, options = {}) {
    const token = getAuthToken();
    
    if (!options.headers) {
        options.headers = {};
    }
    
    if (token) {
        options.headers.Authorization = `Bearer ${token}`;
    }
    
    return fetch(url, options);
}