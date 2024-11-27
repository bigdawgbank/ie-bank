<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row">
        <div class="d-flex justify-content-end mb-3 w-100">
          <button
            type="button"
            class="btn btn-danger btn-sm"
            @click="handleLogout"
          >
            Logout
          </button>
        </div>
        <div class="col-sm-12">
          <h1>Users Management</h1>
          <hr />
          <br />
          <!-- Alert Message -->
          <b-alert v-if="showMessage" :variant="alertVariant" show>{{
            message
          }}</b-alert>

          <button
            type="button"
            class="btn btn-success btn-sm"
            v-b-modal.user-modal
          >
            Create User
          </button>
          <br /><br />
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Username</th>
                <th scope="col">Email</th>
                <th scope="col">Role</th>
                <th scope="col">Account Count</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span
                    :class="
                      user.role === 'admin'
                        ? 'badge badge-primary'
                        : 'badge badge-secondary'
                    "
                    >{{ user.role }}</span
                  >
                </td>
                <td>{{ user.account_count }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      v-b-modal.edit-user-modal
                      @click="editUser(user)"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteUser(user.id)"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <footer class="text-center">
            Copyright &copy; All Rights Reserved.
          </footer>
        </div>
      </div>

      <!-- Create User Modal -->
      <b-modal
        ref="addUserModal"
        id="user-modal"
        title="Create a new user"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmit" class="w-100">
          <b-form-group
            id="form-username-group"
            label="Username:"
            label-for="form-username-input"
          >
            <b-form-input
              id="form-username-input"
              type="text"
              v-model="createUserForm.username"
              placeholder="Username"
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
              type="email"
              v-model="createUserForm.email"
              placeholder="Email"
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
              type="password"
              v-model="createUserForm.password"
              placeholder="Password"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-role-group"
            label="Role:"
            label-for="form-role-input"
          >
            <b-form-select
              id="form-role-input"
              v-model="createUserForm.role"
              :options="roleOptions"
              required
            >
            </b-form-select>
          </b-form-group>
          <b-button type="submit" variant="outline-info">Submit</b-button>
        </b-form>
      </b-modal>

      <!-- Edit User Modal -->
      <b-modal
        ref="editUserModal"
        id="edit-user-modal"
        title="Edit user"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" class="w-100">
          <b-form-group
            id="form-edit-username-group"
            label="Username:"
            label-for="form-edit-username-input"
          >
            <b-form-input
              id="form-edit-username-input"
              type="text"
              v-model="editUserForm.username"
              placeholder="Username"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-edit-email-group"
            label="Email:"
            label-for="form-edit-email-input"
          >
            <b-form-input
              id="form-edit-email-input"
              type="email"
              v-model="editUserForm.email"
              placeholder="Email"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-edit-password-group"
            label="Password: (Leave blank to keep current)"
            label-for="form-edit-password-input"
          >
            <b-form-input
              id="form-edit-password-input"
              type="password"
              v-model="editUserForm.password"
              placeholder="Enter new password"
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-edit-role-group"
            label="Role:"
            label-for="form-edit-role-input"
          >
            <b-form-select
              id="form-edit-role-input"
              v-model="editUserForm.role"
              :options="roleOptions"
              required
            >
            </b-form-select>
          </b-form-group>
          <b-button type="submit" variant="outline-info">Update</b-button>
        </b-form>
      </b-modal>

      <!-- View User Accounts Modal -->
      <b-modal
        ref="viewAccountsModal"
        id="view-accounts-modal"
        title="User Accounts"
        size="lg"
        hide-backdrop
        hide-footer
      >
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Account Name</th>
              <th scope="col">Account Number</th>
              <th scope="col">Balance</th>
              <th scope="col">Currency</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="account in selectedUserAccounts" :key="account.id">
              <td>{{ account.name }}</td>
              <td>{{ account.account_number }}</td>
              <td>{{ account.balance }}</td>
              <td>{{ account.currency }}</td>
              <td>
                <span
                  :class="
                    account.status === 'Active'
                      ? 'badge badge-success'
                      : 'badge badge-danger'
                  "
                  >{{ account.status }}</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </b-modal>
    </div>
  </div>
</template>

<script>
import { adminService, authService } from "../api";

export default {
  name: "AdminPortal",
  data() {
    return {
      users: [],
      selectedUserAccounts: [],
      createUserForm: {
        username: "",
        email: "",
        password: "",
        role: "user",
      },
      editUserForm: {
        id: "",
        username: "",
        email: "",
        password: "",
        role: "",
      },
      showMessage: false,
      message: "",
      alertVariant: "success",
      roleOptions: [
        { value: "user", text: "User" },
        { value: "admin", text: "Admin" },
      ],
    };
  },
  methods: {
    async getUsers() {
      try {
        const response = await adminService.getUsers();
        this.users = response.users;
      } catch (error) {
        console.error("Failed to fetch users:", error);
        this.showError("Failed to fetch users");
      }
    },

    async createUser(payload) {
      try {
        await adminService.createUser(payload);
        await this.getUsers();
        this.showSuccess("User created successfully!");
      } catch (error) {
        console.error("Failed to create user:", error);
        this.showError(error.message || "Failed to create user");
      }
    },

    async updateUser(payload, userId) {
      try {
        await adminService.updateUser(userId, payload);
        await this.getUsers();
        this.showSuccess("User updated successfully!");
      } catch (error) {
        console.error("Failed to update user:", error);
        this.showError(error.message || "Failed to update user");
      }
    },

    async deleteUser(userId) {
      if (confirm("Are you sure you want to delete this user?")) {
        try {
          await adminService.deleteUser(userId);
          await this.getUsers();
          this.showSuccess("User deleted successfully!");
        } catch (error) {
          console.error("Failed to delete user:", error);
          this.showError(error.message || "Failed to delete user");
        }
      }
    },

    async viewUserAccounts(user) {
      try {
        const response = await adminService.getUserAccounts(user.id);
        this.selectedUserAccounts = response.accounts;
        this.$refs.viewAccountsModal.show();
      } catch (error) {
        console.error("Failed to fetch user accounts:", error);
        this.showError("Failed to fetch user accounts");
      }
    },

    async handleLogout() {
      try {
        await authService.logout();
        this.$router.push("/login");
      } catch (error) {
        console.error("Failed to logout:", error);
      }
    },

    initForm() {
      this.createUserForm = {
        username: "",
        email: "",
        password: "",
        role: "user",
      };
      this.editUserForm = {
        id: "",
        username: "",
        email: "",
        password: "",
        role: "",
      };
    },

    async onSubmit(e) {
      e.preventDefault();
      this.$refs.addUserModal.hide();
      await this.createUser(this.createUserForm);
      this.initForm();
    },

    async onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editUserModal.hide();

      const { id, password, ...payload } = this.editUserForm;

      // Only include password if it's provided
      if (password && password.trim() !== "") {
        payload.password = password;
      }

      await this.updateUser(payload, id);
      this.initForm();
    },

    editUser(user) {
      this.editUserForm = {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        password: "", // Initialize empty password
      };
    },

    showSuccess(message) {
      this.message = message;
      this.alertVariant = "success";
      this.showMessage = true;
      setTimeout(() => {
        this.showMessage = false;
      }, 3000);
    },

    showError(message) {
      this.message = message;
      this.alertVariant = "danger";
      this.showMessage = true;
      setTimeout(() => {
        this.showMessage = false;
      }, 3000);
    },
  },

  async created() {
    await this.getUsers();
  },
};
</script>

<style scoped>
.vertical-center {
  min-height: 100vh;
  display: flex;
  align-items: center;
}
</style>
