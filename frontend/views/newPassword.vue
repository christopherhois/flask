<template>
  <div class="auth">
    <h2>Reset Password</h2>
    <form @submit.prevent="resetPassword">
      <div class="form-group">
        <label for="oldPassword">Old Password:</label>
        <input type="password" id="oldPassword" v-model="oldPassword" required />
      </div>
      <div class="form-group">
        <label for="newPassword">New Password:</label>
        <input type="password" id="newPassword" v-model="newPassword" required />
      </div>c
      <div class="form-group">
        <label for="confirmNewPassword">Confirm New Password:</label>
        <input type="password" id="confirmNewPassword" v-model="confirmNewPassword" required />
      </div>
      <button type="submit">Reset Password</button>
    </form>
    <p v-if="error">{{ error }}</p>

    <!-- Modal for showing success message -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>{{ success }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmNewPassword: '',
      error: '',
      success: '',
      token: '',
      showModal: false
    };
  },
  mounted() {
    this.token = this.$route.query.token;
    if (!this.token) {
      this.error = 'Invalid or expired token.';
      this.showModalWithMessage(this.error);
      //this.$router.push({name:'Home'})
    }
  },
  methods: {
    async resetPassword() {
      if (this.newPassword !== this.confirmNewPassword) {
        this.error = 'New passwords do not match.';
        return;
      }
      try {
        const response = await axios.post('http://89.58.1.183:5000/api/newpassword', {
          oldPassword: this.oldPassword,
          newPassword: this.newPassword,
          token: this.token
        });
        this.success = response.data.msg;
        this.showModalWithMessage(response.data.msg);
      } catch (error) {
        this.error = error.response ? error.response.data.msg : 'Password reset failed. Please try again.';
        console.log(this.error)
      }
    },
    showModalWithMessage(message) {
      this.success = message;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>

<style scoped>
.auth {
  background-color: #2b2b2b; /* Dark Mode Hintergrundfarbe */
  color: #f2f2f2; /* Helle Textfarbe für Kontrast */
  font-family: 'Arial', sans-serif; /* Saubere und moderne Schriftart */
  padding: 20px;
  border-radius: 10px; /* Abgerundete Ecken */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sanfter Schatten */
  max-width: 400px;
  margin: 50px auto;
  text-align: center; /* Zentriere den Text */
}

h2 {
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left; /* Linksbündige Labels */
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="password"] {
  width: 100%; /* Verhindert, dass die Eingabefelder über den Container hinausragen */
  padding: 10px;
  border: 1px solid #555;
  border-radius: 5px;
  background-color: #3b3b3b;
  color: #f2f2f2;
  box-sizing: border-box; /* Enthält Padding und Border in der Breitenberechnung */
}

button {
  width: 100%; /* Buttons nehmen jeweils 48% des verfügbaren Platzes ein */
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #1e90ff;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #1c7ed6;
}

p {
  color: red;
  text-align: center;
  margin-top: 15px;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 300px;
  text-align: center;
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

/* Responsive Design */
@media (max-width: 600px) {
  .auth {
    padding: 10px;
    margin: 20px auto;
    box-shadow: none;
  }

  input, button {
    padding: 8px;
  }
}
</style>
