import axios from "axios";

const api = axios.create({
  withCredentials: true,
  baseURL: process.env.VUE_APP_ROOT_API,
  headers: {
    Accept: "application/json",
  },
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
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async logout() {
    try {
      const response = await api.post("/logout");
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  async checkSession() {
    try {
      const response = await api.get("/session");
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },
};

export const accountService = {
  async getAccounts() {
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
