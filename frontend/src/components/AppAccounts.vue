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
          <h1>Accounts</h1>
          <hr />
          <br />
          <!-- Alert Message -->
          <b-alert v-if="showMessage" variant="success" show>
            {{ message }}
          </b-alert>

          <button
            type="button"
            class="btn btn-success btn-sm"
            v-b-modal.account-modal
          >
            Create Account
          </button>
          <button
            type="button"
            class="btn btn-primary btn-sm"
            v-b-modal.transfer-modal
          >
            Transfer Money
          </button>


          <button
            type="button"
            class="btn btn-primary btn-sm"
            @click="refreshAccounts"
          >
            Refresh Accounts
          </button>

          <br /><br />
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Account Name</th>
                <th scope="col">Account Number</th>
                <th scope="col">Account Balance</th>
                <th scope="col">Account Currency</th>
                <th scope="col">Account Status</th>
                <th scope="col">Account Country</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="account in accounts" :key="account.id">
                <td>{{ account.name }}</td>
                <td>{{ account.account_number }}</td>
                <td>{{ account.balance }}</td>
                <td>{{ account.currency }}</td>
                <td>
                  <span
                    v-if="account.status == 'Active'"
                    class="badge badge-success"
                    >{{ account.status }}</span
                  >
                  <span v-else class="badge badge-danger">{{
                    account.status
                  }}</span>
                </td>
                <td>{{ account.country }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      v-b-modal.edit-account-modal
                      @click="editAccount(account)"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteAccount(account.id)"
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
      <b-modal
        ref="addAccountModal"
        id="account-modal"
        title="Create a new account"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmit" class="w-100">
          <b-form-group
            id="form-name-group"
            label="Account Name:"
            label-for="form-name-input"
          >
            <b-form-input
              id="form-name-input"
              type="text"
              v-model="createAccountForm.name"
              placeholder="Account Name"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-currency-group"
            label="Currency:"
            label-for="form-currency-input"
          >
            <b-form-input
              id="form-currency-input"
              type="text"
              v-model="createAccountForm.currency"
              placeholder="$ or €"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-form-group
            id="form-country-group"
            label="Country:"
            label-for="form-country-input"
          >
            <b-form-input
              id="form-country-input"
              type="text"
              v-model="createAccountForm.country"
              placeholder="Your Country"
              required
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-balance-group"
            label="Balance:"
            label-for="form-balance-input"
          >
            <b-form-input
              id="form-balance-input"
              type="text"
              v-model="createAccountForm.balance"
              placeholder="0"
              required
            >
            </b-form-input>
          </b-form-group>





          <b-button type="submit" variant="outline-info">Submit</b-button>
        </b-form>
      </b-modal>
      <!-- End of Modal for Create Account-->
      <!-- Start of Modal for Edit Account-->
      <b-modal
        ref="editAccountModal"
        id="edit-account-modal"
        title="Edit the account"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" class="w-100">
          <b-form-group
            id="form-edit-name-group"
            label="Account Name:"
            label-for="form-edit-name-input"
          >
            <b-form-input
              id="form-edit-name-input"
              type="text"
              v-model="editAccountForm.name"
              placeholder="Account Name"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-button type="submit" variant="outline-info">Update</b-button>
        </b-form>
      </b-modal>
      <!-- End of Modal for Edit Account-->
      <!-- Start of Modal for Transfer Money-->
      <b-modal
        ref="transferModal"
        id="transfer-modal"
        title="Transfer Money"
        hide-backdrop
        hide-footer
      >
        <Transfer />
      </b-modal>
      <!-- End of Modal for Transfer Money-->
    </div>
  </div>
</template>

<script>
import { accountService, authService } from "../api"; // Import your API client
import Transfer from "./Transfer.vue"; // Import the Transfer component

export default {
  name: "AppAccounts",
  components: {
    Transfer,
  },
  data() {
    return {
      accounts: [],
      createAccountForm: {
        name: "",
        currency: "",
        country: "",
        balance: "",
      },
      editAccountForm: {
        id: "",
        name: "",
      },
      showMessage: false,
      message: "",
    };
  },
  methods: {
    // Get all accounts
    async getAccounts() {
      try {
        const response = await accountService.getAccounts();
        console.log(response);
        this.accounts = response.accounts;
      } catch (error) {
        console.error("Failed to fetch accounts:", error);
        // Optionally show error message to user
      }
    },
    refreshAccounts() {
      this.getAccounts();
    },

    // Create new account
    async createAccount(payload) {
      try {
        await accountService.createAccount(payload);
        await this.getAccounts(); // Refresh the list

        // Show success message
        this.message = "Account Created successfully!";
        this.showMessage = true;
        setTimeout(() => {
          this.showMessage = false;
        }, 3000);
      } catch (error) {
        console.error("Failed to create account:", error);
        // Optionally show error message to user
      }
    },

    // Update account
    async updateAccount(payload, accountId) {
      try {
        await accountService.updateAccount(accountId, payload);
        await this.getAccounts(); // Refresh the list

        // Show success message
        this.message = "Account Updated successfully!";
        this.showMessage = true;
        setTimeout(() => {
          this.showMessage = false;
        }, 3000);
      } catch (error) {
        console.error("Failed to update account:", error);
        // Optionally show error message to user
      }
    },

    // Delete account
    async deleteAccount(accountId) {
      try {
        await accountService.deleteAccount(accountId);
        await this.getAccounts(); // Refresh the list

        // Show success message
        this.message = "Account Deleted successfully!";
        this.showMessage = true;
        setTimeout(() => {
          this.showMessage = false;
        }, 3000);
      } catch (error) {
        console.error("Failed to delete account:", error);
        // Optionally show error message to user
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

    // Initialize forms empty
    initForm() {
      this.createAccountForm.name = "";
      this.createAccountForm.currency = "";
      this.createAccountForm.country = "";
      this.createAccountForm.balance = 0;
      this.editAccountForm.id = "";
      this.editAccountForm.name = "";
    },

    // Handle submit event for create account
    async onSubmit(e) {
      e.preventDefault();
      this.$refs.addAccountModal.hide();

      const payload = {
        name: this.createAccountForm.name,
        currency: this.createAccountForm.currency,
        country: this.createAccountForm.country,
        balance: this.createAccountForm.balance,
      };

      await this.createAccount(payload);
      this.initForm();
    },

    // Handle submit event for edit account
    async onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editAccountModal.hide();

      const payload = {
        name: this.editAccountForm.name,
      };

      await this.updateAccount(payload, this.editAccountForm.id);
      this.initForm();
    },

    // Handle edit button
    editAccount(account) {
      this.editAccountForm = account;
    },

    // Handle Delete button
    async handleDelete(account) {
      await this.deleteAccount(account.id);
    },
  },

  // Lifecycle hooks
  async created() {
    await this.getAccounts();
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