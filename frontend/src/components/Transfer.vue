<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card custom-width">
            <div class="card-header">
              <h3 class="text-center">Transfer between my accounts</h3>
            </div>
            <div class="card-body">
              <!-- Alert Messages -->
              <b-alert v-if="showMessage" :variant="alertVariant" show>
                <div v-html="message"></div>
              </b-alert>

              <!-- Transfer Form -->
              <b-form @submit="onSubmit">
                <b-form-group
                  id="form-sender-account-id-group"
                  label="Origin Account:"
                  label-for="form-sender-account-id-input"
                >
                  <b-form-select
                    id="form-sender-account-id-input"
                    v-model="transferForm.sender_account_id"
                    :options="
                      accounts.map((account) => ({
                        value: account.id,
                        text: account.name,
                      }))
                    "
                    required
                  ></b-form-select>
                </b-form-group>

                <b-form-group
                  id="form-recipient-account-id-group"
                  label="Recipient Account:"
                  label-for="form-recipient-account-id-input"
                >
                  <b-form-select
                    id="form-recipient-account-id-input"
                    v-model="transferForm.recipient_account_id"
                    :options="
                      accounts.map((account) => ({
                        value: account.id,
                        text: account.name,
                      }))
                    "
                    required
                  ></b-form-select>
                </b-form-group>

                <b-form-group
                  id="form-amount-group"
                  label="Amount:"
                  label-for="form-amount-input"
                >
                  <b-form-input
                    id="form-amount-input"
                    v-model.number="transferForm.amount"
                    type="number"
                    placeholder="Enter amount"
                    min="0"
                    required
                  ></b-form-input>
                </b-form-group>

                <div class="text-center">
                  <b-button type="submit" variant="primary" class="w-100">
                    Transfer
                  </b-button>
                </div>
              </b-form>
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
import { transferService, accountService } from "../api";

export default {
  name: "Transfer",
  data() {
    return {
      transferForm: {
        sender_account_id: "",
        recipient_account_id: "",
        amount: 0,
      },
      showMessage: false,
      message: "",
      alertVariant: "danger",
      accounts: [],
    };
  },
  methods: {
    async fetchAccounts() {
      try {
        //alert("fetching accounts");
        const response = await accountService.getUserAccounts();
        console.log(response);
        this.accounts = response.accounts;
      } catch (error) {
        console.error("Error fetching accounts:", error);
      }
    },
    async onSubmit(e) {
      e.preventDefault();

      try {
        //alert("transferring money");
        //alert(this.transferForm);
        const response = await transferService.transferMoney(this.transferForm);

        // Show success message
        this.message = "Transfer successful!";
        this.alertVariant = "success";
        this.showMessage = true;

        // Emit change to parent component
        this.$emit("transfer-completed");

        // Display receipt
        this.message += `
            <br>Receipt:
            <ul>
              <li>Sender Account ID: ${response.receipt.sender_account_id}</li>
              <li>Recipient Account ID: ${response.receipt.recipient_account_id}</li>
              <li>Amount: ${response.receipt.amount}</li>
              <li>Timestamp: ${response.receipt.timestamp}</li>
            </ul>
          `;
      } catch (error) {
        // Show error message
        this.message = error.message || "Transfer failed";
        this.alertVariant = "danger";
        this.showMessage = true;

        // Hide error after 3 seconds
        setTimeout(() => {
          this.showMessage = false;
        }, 3000);
      }
    },
  },
  mounted() {
    this.fetchAccounts();
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
.custom-width {
  width: 80%; /* Adjust the width as needed */
}
</style>

