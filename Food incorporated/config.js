/**
 * Configuration file for domain-based API access
 * Automatically detects the current domain and constructs API URLs
 * 
 * Usage in HTML: <script src="../config.js"></script>
 * Then use: CONFIG.API_URL, CONFIG.ORDERS_URL, CONFIG.TABLES_URL
 */

const CONFIG = (() => {
    // Detect if running in production or development
    const isDevelopment = window.location.hostname === 'localhost' || 
                          window.location.hostname === '127.0.0.1';
    
    const protocol = window.location.protocol; // http: or https:
    const hostname = window.location.hostname;
    
    // Construct base API URL from current domain
    let apiPort = ':5000'; // Default Flask port
    let apiUrl;
    
    if (isDevelopment) {
        // In development: use localhost:5000
        apiUrl = `${protocol}//localhost:5000`;
    } else {
        // In production: use same domain as frontend
        // Assumes backend is served on same domain (via reverse proxy or subdomain)
        apiUrl = `${protocol}//${hostname}`;
    }
    
    return {
        // Base API URL
        API_URL: apiUrl,
        
        // Specific endpoints
        ORDERS_URL: `${apiUrl}/orders`,
        TABLES_URL: `${apiUrl}/tables`,
        STOCK_URL: `${apiUrl}/stock`,
        HEALTH_URL: `${apiUrl}/health`,
        
        // Development flag
        IS_DEVELOPMENT: isDevelopment,
        
        // Current hostname (useful for logging/debugging)
        HOSTNAME: hostname,
        PROTOCOL: protocol,
        
        // Helper method to construct endpoint URLs
        getEndpoint: function(path) {
            return `${this.API_URL}${path}`;
        }
    };
})();

// Make CONFIG globally available
window.CONFIG = CONFIG;

console.log('[CONFIG] Initialized with API URL:', CONFIG.API_URL);
