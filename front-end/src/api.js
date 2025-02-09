import axios from 'axios';
import router from '@/router';  // Import your Vue Router instance

// Create an Axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // API base URL from .env
  withCredentials: true, // Include HttpOnly cookies with requests
});

// Response interceptor to handle token refresh on 401 errors
api.interceptors.response.use(
  (response) => response, // Return response if it's successful
  async (error) => {
    const originalRequest = error.config;

    // Check for a 401 error and ensure we haven't already retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Prevent infinite loops

      try {
        // Attempt to refresh the token by posting to the refresh endpoint.
        await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/auth/refresh/`,
          {},
          { withCredentials: true }
        );
        // If refresh is successful, retry the original request.
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed. Redirecting to login...', refreshError);
        // Redirect the user to the login page.
        router.push("/");
        return Promise.reject(refreshError);
      }
    }

    // If the error is not a 401 or the request has already been retried, reject it.
    return Promise.reject(error);
  }
);

export default api;
