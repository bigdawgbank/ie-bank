<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card custom-width">
            <div class="card-header">
              <h3 class="text-center">Wire Transfer</h3>
            </div>
            <div class="card-body">
              <!-- Alert Messages -->
              <b-alert v-if="showMessage" :variant="alertVariant" show>
                <div v-html="message"></div>
              </b-alert>

              <!-- WireTransfer Form -->
              <b-form @submit="onSubmit">
                <b-form-group
                  id="form-sender-account-id-group"
                  label="Origin Account:"
                  label-for="form-sender-account-id-input"
                >
                  <b-form-select
                    id="form-sender-account-id-input"
                    v-model="wireTransferForm.sender_account_id"
                    :options="
                      accounts.map((account) => ({
                        value: account.id,
                        text: account.account_number,
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
                  <b-form-input
                    id="form-recipient-account-id-input"
                    v-model="wireTransferForm.recipient_account_number"
                    type="text"
                    required
                  ></b-form-input>
                </b-form-group>

                <b-form-group
                  id="form-amount-group"
                  label="Origin Amount:"
                  label-for="form-amount-input"
                >
                  <b-form-input
                    id="form-amount-input"
                    v-model.number="wireTransferForm.amount"
                    type="number"
                    placeholder="Enter amount"
                    min="0"
                    required
                  ></b-form-input>
                </b-form-group>

                <b-form-group
                  id="form-exchange-rate-group"
                  label="Exchange Rate:"
                  label-for="form-exchange-rate-input"
                >
                  <b-form-input
                    id="form-exchange-rate-input"
                    v-model="exchangeRate"
                    type="text"
                    readonly
                  ></b-form-input>
                </b-form-group>

                <b-form-group
                  id="form-converted-amount-group"
                  label="Converted Amount:"
                  label-for="form-converted-amount-input"
                >
                  <b-form-input
                    id="form-converted-amount-input"
                    v-model="convertedAmount"
                    type="text"
                    readonly
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
import { wireTransferService, accountService, exchangeRateService } from "../api";

export default {
  name: "WireTransfer",
  data() {
    return {
      wireTransferForm: {
        sender_account_id: "",
        recipient_account_number: "",
        amount: 0,
      },
      showMessage: false,
      message: "",
      alertVariant: "danger",
      accounts: [],
      exchangeRate: 1,
      convertedAmount: 0,
    };
  },
  methods: {
    async fetchAccounts() {
      try {
        const response = await accountService.getUserAccounts();
        console.log(response);
        this.accounts = response.accounts;
      } catch (error) {
        console.error("Error fetching accounts:", error);
      }
    },

    async fetchExchangeRate() {

      if (!this.wireTransferForm.sender_account_id || !this.wireTransferForm.recipient_account_number) {
          return;
        }

      try {
        const senderAccount = this.accounts.find(account => account.id === this.wireTransferForm.sender_account_id);
        const recipientAccount = await accountService.getAccountByNumber(this.wireTransferForm.recipient_account_number);

        const response = await exchangeRateService.getExchangeRate(senderAccount.currency, recipientAccount.currency);
        this.exchangeRate = response.exchange_rate;
        this.calculateConvertedAmmount();
      } catch (error) {
        console.error("Error fetching exchange rate:", error);
      }
    },

    async calculateConvertedAmmount() {
      try {
        this.convertedAmount = this.wireTransferForm.amount * this.exchangeRate;
      } catch (error) {
        console.error("Error calculating converted ammount:", error);
      }
    },

    async onSubmit(e) {
      e.preventDefault();
      await this.fetchExchangeRate();

      try {
        const response = await wireTransferService.wireTransferMoney(this.wireTransferForm);

        // Show success message
        this.message = `
          Wire Transfer successful!<br>Receipt:
          <ul>
            <li>Sender Account ID: ${response.receipt.sender_account_id}</li>
            <li>Recipient Account Number: ${response.receipt.recipient_account_number}</li>
            <li>Amount: ${response.receipt.amount}</li>
            <li>Converted Amount: ${this.convertedAmount}</li>
            <li>Exchange Rate: ${this.exchangeRate}</li>
            <li>Timestamp: ${response.receipt.timestamp}</li>
          </ul>
        `;
        this.alertVariant = "success";
        this.showMessage = true;

        // Emit change to parent component
        this.$emit("transfer-completed");

      } catch (error) {
        // Show error message
        this.message = "Wire Transfer failed. Please try again.";
        this.alertVariant = "danger";
        this.showMessage = true;
      }

      // Hide message after 3 seconds
      setTimeout(() => {
        this.showMessage = false;
      }, 3000);
    },
  },
  watch: {
    'wireTransferForm.sender_account_id': 'fetchExchangeRate',
    'wireTransferForm.recipient_account_number': 'fetchExchangeRate',
    'wireTransferForm.amount': 'calculateConvertedAmmount',
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