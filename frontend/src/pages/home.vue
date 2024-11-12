<template>
  <div class="auth">
    <div v-if="isLogin">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="input">Email or Username:</label>
          <input type="text" id="input" v-model="input" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <div class="form-group">
          <input type="checkbox" id="rememberMe" v-model="rememberMe" />
          <label for="rememberMe">Remember Me</label>
        </div>
        <div class="button-group">
          <button type="submit">Login</button>
          <button @click="googleLogin" type="button" class="google-button">Login with Google</button>
        </div>
      </form>
      <p v-if="error">{{ error }}</p>

    </div>

    <!-- register toggle not necessary anymore
    <p><a @click="toggleAuth">Need an account? Register here.</a></p>
    <div v-else>
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Register</button>
      </form>
      <p v-if="error">{{ error }}</p>
      <p><a @click="toggleAuth">Already have an account? Login here.</a></p>
    </div>  -->
    <p>
      <router-link to="/admin">Admin</router-link>
    </p>
    <p>
      <router-link to="/reset-password">password</router-link>
    </p>

    <!-- Modal for showing messages -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>{{ modalMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      input: '',
      email: '',
      password: '',
      username: '',
      error: '',
      isLogin: true,
      rememberMe: false,
      showModal: false,
      modalMessage: '',
    };
  },
  methods: {
    toggleAuth() {
      this.isLogin = !this.isLogin;
    },
    async login() {
      try {
        const response = await axios.post('http://89.58.1.183:5000/api/auth/login', {
          input: this.input,
          password: this.password
        });

        if (response.data.token) {
          if (this.rememberMe) {
            localStorage.setItem('token', response.data.token);
          } else {
            sessionStorage.setItem('token', response.data.token);
          }

          this.$router.push('/');
        } else {
          this.error = response.data.msg;
          this.showModalWithMessage('Login failed. Please check your credentials.');
        }
      } catch (error) {
        this.error = error.response ? error.response.data.msg : 'Login failed. Please check your credentials.';
        this.showModalWithMessage(this.error);
      }
    },

    /*register was moved to Admin
    async register() {
      try {
        const response = await axios.post('http://89.58.1.183:5000/api/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        console.log(response.data); // Debugging line
        this.isLogin = true;
        console.log("Test successful");
        this.showModalWithMessage('Registration successful! Please check your email for confirmation.');
      }  catch (error) {
        console.log(error.response.data); // Debugging line
        this.error = error.response ? error.response.data.msg : 'Registration failed. Please try again.';
        this.showModalWithMessage(this.error);
      }
    },*/

    showModalWithMessage(message) {
      this.modalMessage = message;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    //googleLogin() {
    //  window.location.href = 'auth/google';
    //}
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

input[type="email"], input[type="password"], input[type="text"] {
  width: 100%; /* Verhindert, dass die Eingabefelder über den Container hinausragen */
  padding: 10px;
  border: 1px solid #555;
  border-radius: 5px;
  background-color: #3b3b3b;
  color: #f2f2f2;
  box-sizing: border-box; /* Enthält Padding und Border in der Breitenberechnung */
}

input[type="checkbox"] {
  margin-right: 10px;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

button {
  width: 48%; /* Buttons nehmen jeweils 48% des verfügbaren Platzes ein */
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

.google-button {
  background-color: #1c7ed6; /* Dunklerer Blauton */
}

.google-button:hover {
  background-color: #1e90ff; /* Gleiche Farbe wie der andere Button beim Hover */
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