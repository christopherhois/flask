<template>
  <div class="admin">
    <h1>Admin Dashboard</h1>

    <button class="current-week">{{ currentWeek }}</button>

    <div class="section">
      <h4>Neuen Kunden hinzufügen</h4>
      <form @submit.prevent="addEnergieversorger" class="add-customer-form">
        <input type="text" v-model="newEnergieversorger" class="half-width-input" placeholder="Trage hier einen neuen Kunden ein" required />
        <button type="submit">Hinzufügen</button>
      </form>
    </div>

    <div class="section">
      <h4>Neuen Mitarbeiter hinzufügen</h4>
      <form @submit.prevent="register" class="add-employee-form">
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
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <div class="section">
      <h4>Kundenliste</h4>
      <ul class="customer-list">
        <li v-for="ev in energieversorger" :key="ev._id" class="customer-item">
          {{ ev.name }}
          <div class="dropdown">
            <button @click="editEnergieversorger(ev._id)">Bearbeiten</button>
            <button @click="removeEnergieversorger(ev._id)">Entfernen</button>
          </div>
        </li>
      </ul>
    </div>

    <div class="section">
      <h4>PT Checks Übersicht</h4>
      <table>
        <thead>
        <tr>
          <th>Kunde</th>
          <th v-for="user in users" :key="user._id">
            <div>
              <input type="checkbox" :checked="user.isAdmin" @change="toggleAdmin(user._id)" /> Admin
              <input type="checkbox" :checked="user.isHR" @change="toggleHR(user._id)" /> HR
            </div>
            {{ user.username }}
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="ev in energieversorger" :key="ev._id">
          <td>{{ ev.name }}</td>
          <td v-for="user in users" :key="user._id">{{ getUserPTCheck(user._id, ev.name) }}</td>
        </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>{{ modalMessage }}</p>
      </div>
    </div>

    <p>
      <router-link to="/">Home</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Admin',
  data() {
    return {
      newEnergieversorger: '',
      energieversorger: [],
      users: [],
      ptChecks: [],
      currentWeek: '',
      username: '',
      email: '',
      password: '',
      error: '',
      showModal: false,
      modalMessage: ''
    };
  },
  mounted() {
    //checking for logged in status and sending user back to auth if not logged in
    let userLocal = localStorage.getItem('token');
    let userSession = sessionStorage.getItem('token');
    if (!(userLocal || userSession)){
      this.$router.push({name:'Auth'})
    }
    this.loadEnergieversorger();
    this.loadUsers();
    this.loadPTChecks();
    this.getCurrentWeek();

  },
  methods: {
    async loadEnergieversorger() {
      try {
        const response = await fetch('http://89.58.1.183:5000/api/energieversorger/');
        this.energieversorger = await response.json();
      } catch (err) {
        console.error('Error loading energieversorger:', err);
      }
    },
    async addEnergieversorger() {
      try {
        const response = await fetch('http://89.58.1.183:5000/api/energieversorger/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.newEnergieversorger })
        });

        if (!response.ok) {
          throw new Error(`Server error: ${response.statusText}`);
        }

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new Error(`Expected JSON, but got ${contentType}`);
        }

        const energieversorger = await response.json();
        this.energieversorger.push(energieversorger);
        this.newEnergieversorger = '';
      } catch (err) {
        console.error('Error adding energieversorger:', err);
      }
    },
    async removeEnergieversorger(id) {
      try {
        await fetch(`http://89.58.1.183:5000/api/energieversorger/${id}`, {
          method: 'DELETE'
        });
        this.energieversorger = this.energieversorger.filter(ev => ev._id !== id);
      } catch (err) {
        console.error('Error removing energieversorger:', err);
      }
    },
    async loadUsers() {
      try {
        const response = await fetch('http://89.58.1.183:5000/api/admnin/users');
        this.users = await response.json();
      } catch (err) {
        console.error('Error loading users:', err);
      }
    },
    async loadPTChecks() {
      try {
        const response = await fetch('http://89.58.1.183:5000/api/pt-check/current');
        this.ptChecks = await response.json();
      } catch (err) {
        console.error('Error loading PT checks:', err);
      }
    },
    getUserPTCheck(userId, energieversorger) {
      const ptCheck = this.ptChecks.find(pt => pt.user._id === userId && pt.energieVersorger === energieversorger);
      return ptCheck ? ptCheck.werFakturiert : 0;
    },
    async toggleAdmin(userId) {
      try {
        const user = this.users.find(u => u._id === userId);
        user.isAdmin = !user.isAdmin;
        await fetch(`/api/auth/users/${userId}/admin`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ isAdmin: user.isAdmin })
        });
      } catch (err) {
        console.error('Error toggling admin:', err);
      }
    },
    async toggleHR(userId) {
      try {
        const user = this.users.find(u => u._id === userId);
        user.isHR = !user.isHR;
        await fetch(`/api/auth/users/${userId}/hr`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ isHR: user.isHR })
        });
      } catch (err) {
        console.error('Error toggling HR:', err);
      }
    },
    getCurrentWeek() {
      const currentDate = new Date();
      const startDate = new Date(currentDate.getFullYear(), 0, 1);
      const days = Math.floor((currentDate - startDate) / (24 * 60 * 60 * 1000));
      const weekNumber = Math.ceil(days / 7);
      this.currentWeek = `Woche ${weekNumber}`;
    },
    async register() {
      try {
        const response = await axios.post('http://89.58.1.183:5000/api/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.isLogin = true;
        this.showModalWithMessage('Registration successful! Please check your email for confirmation.');
      } catch (error) {
        this.error = error.response ? error.response.data.msg : 'Registration failed. Please try again.';
        this.showModalWithMessage(this.error);
      }
    },
    showModalWithMessage(message) {
      this.modalMessage = message;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>

<style scoped>
.admin {
  background-color: #2b2b2b;
  color: #f2f2f2;
  font-family: 'Arial', sans-serif;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  text-align: center;
  max-width: 1000px;
  margin: 20px auto; /* Add some margin to the top and bottom */
}

.current-week {
  background-color: #1e90ff;
  color: #fff;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 20px; /* Add margin to the bottom */
}

.current-week:hover {
  background-color: #1c7ed6;
}

h1, h2 {
  text-align: center;
  margin-bottom: 20px; /* Add margin to the bottom */
}

.section {
  margin-bottom: 30px; /* Add space between sections */
}

.add-customer-form,
.add-employee-form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  max-width: 500px; /* Max width for form alignment */
  margin: 0 auto; /* Center the form horizontally */
}

.form-group {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  margin-bottom: 10px;
}

label {
  margin-right: 10px;
  min-width: 100px; /* Minimum width for labels */
  text-align: left;
}

input[type="text"], input[type="email"], input[type="password"], input[type="checkbox"] {
  flex: 1;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #555;
  border-radius: 5px;
  background-color: #3b3b3b;
  color: #f2f2f2;
}

button {
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

.error {
  color: red;
  margin-top: 10px;
}

.customer-list {
  list-style-type: none;
  padding: 0;
}

.customer-item {
  position: relative;
  display: inline-block;
  margin: 10px 0;
}

.customer-item:hover .dropdown {
  display: block;
}

.dropdown {
  display: none;
  position: absolute;
  background-color: #3b3b3b;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown button {
  color: white;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  background-color: #1e90ff;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

th, td {
  border: 1px solid #555;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #444;
  color: #f2f2f2;
}

tfoot td {
  font-weight: bold;
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
  .admin {
    padding: 10px;
    margin: 10px;
  }

  input, button {
    padding: 8px;
  }

  .form-group {
    flex-direction: column;
    align-items: flex-start;
  }

  label {
    margin-bottom: 5px;
  }

  .dropdown {
    position: static;
    display: block;
  }
}
</style>
