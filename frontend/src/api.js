import axios from "axios";

const api = axios.create({
  baseURL: process.env.VUE_APP_ROOT_API,
  headers: {
    Accept: "application/json",
  },
});

// Add interceptor to add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  async register(userData) {
    try {
      const response = await api.post("/register", userData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async login(credentials) {
    try {
      const response = await api.post("/login", credentials);
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
      }
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  // Add this new method
  async getProfile() {
    try {
      const response = await api.get("/profile");
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  logout() {
    localStorage.removeItem("token");
  },

  checkSession() {
    return !!localStorage.getItem("token");
  },
};

export const accountService = {
  async getUserAccounts() {
    try {
      const response = await api.get("/accounts");
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async createAccount(accountData) {
    try {
      const response = await api.post("/accounts", accountData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async getAccount(id) {
    try {
      const response = await api.get(`/accounts/${id}`);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async updateAccount(id, accountData) {
    try {
      const response = await api.put(`/accounts/${id}`, accountData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async deleteAccount(id) {
    try {
      const response = await api.delete(`/accounts/${id}`);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },
};

export const adminService = {
  // Get all users
  async getUsers() {
    try {
      const response = await api.get("/users");
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get specific user details
  async getUser(userId) {
    try {
      const response = await api.get(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Create new user
  async createUser(userData) {
    try {
      const response = await api.post("/users", userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Update user
  async updateUser(userId, userData) {
    try {
      const response = await api.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Delete user
  async deleteUser(userId) {
    try {
      const response = await api.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Update account status
  async updateAccountStatus(userId, accountId, statusData) {
    try {
      const response = await api.patch(
        `/users/${userId}/accounts/${accountId}/status`,
        statusData
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get all accounts (including other users')
  async getAllAccounts() {
    try {
      const response = await api.get("/accounts/all");
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get accounts for specific user
  async getUserAccounts(userId) {
    try {
      const response = await api.get(`/users/${userId}/accounts`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
};
export const transferService = {
  async transferMoney(transferData) {
    try {
      const response = await api.post("/transfer", transferData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },
};
export const wireTransferService = {
  async wireTransferMoney(wireTransferData) {
    try {
      const response = await api.post("/wiretransfer", wireTransferData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },
};