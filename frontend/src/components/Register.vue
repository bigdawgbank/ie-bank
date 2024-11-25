<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3 class="text-center">Register</h3>
            </div>
            <div class="card-body">
              <!-- Alert Messages -->
              <b-alert v-if="showMessage" :variant="alertVariant" show>
                {{ message }}
              </b-alert>

              <!-- Registration Form -->
              <b-form @submit="onSubmit">
                <b-form-group
                  id="form-username-group"
                  label="Username:"
                  label-for="form-username-input"
                >
                  <b-form-input
                    id="form-username-input"
                    v-model="registerForm.username"
                    type="text"
                    placeholder="Choose a username"
                    required
                  >
                  </b-form-input>
                </b-form-group>

                <b-form-group
                  id="form-email-group"
                  label="Email:"
                  label-for="form-email-input"
                >
                  <b-form-input
                    id="form-email-input"
                    v-model="registerForm.email"
                    type="email"
                    placeholder="Enter your email"
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
                    v-model="registerForm.password"
                    type="password"
                    placeholder="Choose a password"
                    required
                  >
                  </b-form-input>
                  <small class="form-text text-muted">
                    Password must be at least 8 characters and include
                    uppercase, lowercase, and numbers.
                  </small>
                </b-form-group>

                <div class="text-center">
                  <b-button type="submit" variant="success" class="w-100">
                    Register
                  </b-button>
                </div>
              </b-form>

              <div class="text-center mt-3">
                <p class="mb-0">
                  Already have an account?
                  <router-link to="/login">Login here</router-link>
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
  name: "Register",
  data() {
    return {
      registerForm: {
        username: "",
        email: "",
        password: "",
      },
      showMessage: false,
      message: "",
      alertVariant: "danger",
    };
  },
  methods: {
    validatePassword() {
      if (this.registerForm.password.length < 8) {
        throw new Error("Password must be at least 8 characters long");
      }
      if (!/[A-Z]/.test(this.registerForm.password)) {
        throw new Error("Password must contain at least one uppercase letter");
      }
      if (!/[a-z]/.test(this.registerForm.password)) {
        throw new Error("Password must contain at least one lowercase letter");
      }
      if (!/[0-9]/.test(this.registerForm.password)) {
        throw new Error("Password must contain at least one number");
      }
    },

    async onSubmit(e) {
      e.preventDefault();

      try {
        // Validate password
        this.validatePassword();
        const formData = new FormData();
        formData.append("username", this.registerForm.username);
        formData.append("email", this.registerForm.email);
        formData.append("password", this.registerForm.password);

        // Send registration request
        await authService.register(formData);

        // Show success message
        this.message = "Registration successful!";
        this.alertVariant = "success";
        this.showMessage = true;

        // Redirect to login page
        setTimeout(() => {
          this.$router.push("/login");
        }, 1500);
      } catch (error) {
        // Show error message
        this.message = error.message || "Registration failed";
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
