<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3 class="text-center">Login</h3>
            </div>
            <div class="card-body">
              <!-- Alert Messages -->
              <b-alert v-if="showMessage" :variant="alertVariant" show>
                {{ message }}
              </b-alert>

              <!-- Login Form -->
              <b-form @submit="onSubmit">
                <b-form-group
                  id="form-username-group"
                  label="Username:"
                  label-for="form-username-input"
                >
                  <b-form-input
                    id="form-username-input"
                    v-model="loginForm.username"
                    type="text"
                    placeholder="Enter username"
                    required
                  >
                  </b-form-input>
                </b-form-group>

                <b-form-group
                  id="form-password-group"
                  label="Password:"
                  label-for="form-password-input"
                >
                  <b-form-input
                    id="form-password-input"
                    v-model="loginForm.password"
                    type="password"
                    placeholder="Enter password"
                    required
                  >
                  </b-form-input>
                </b-form-group>

                <div class="text-center">
                  <b-button type="submit" variant="primary" class="w-100">
                    Login
                  </b-button>
                </div>
              </b-form>

              <div class="text-center mt-3">
                <p class="mb-0">
                  Don't have an account?
                  <router-link to="/register">Register here</router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <footer class="text-center mt-5">
        Copyright &copy; All Rights Reserved.
      </footer>
    </div>
  </div>
</template>

<script>
import { authService } from "../api";

export default {
  name: "Login",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      showMessage: false,
      message: "",
      alertVariant: "danger",
    };
  },
  methods: {
    async onSubmit(e) {
      e.preventDefault();

      try {
        const formData = new FormData();
        formData.append("username", this.loginForm.username);
        formData.append("password", this.loginForm.password);
        await authService.login(formData);

        // Show success message
        this.message = "Login successful!";
        this.alertVariant = "success";
        this.showMessage = true;

        // Redirect to accounts page
        setTimeout(() => {
          this.$router.push("/accounts");
        }, 1000);
      } catch (error) {
        // Show error message
        this.message = error.error || "Login failed";
        this.alertVariant = "danger";
        this.showMessage = true;

        // Hide error after 3 seconds
        setTimeout(() => {
          this.showMessage = false;
        }, 3000);
      }
    },
  },
};
</script>

<style scoped>
.vertical-center {
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.card {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}
</style>
