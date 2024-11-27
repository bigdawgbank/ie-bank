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