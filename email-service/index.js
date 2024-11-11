const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'karottensaft.matrix@gmail.com',
    pass: 'dein_passwort'
  }
});

app.post('/send-email', (req, res) => {
  const { to, subject, text } = req.body;

  const mailOptions = {
    from: 'karottensaft.matrix@gmail.com',
    to,
    subject,
    text
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Fehler beim Senden der E-Mail:', error);
      res.status(500).send('Fehler beim Senden der E-Mail');
    } else {
      console.log('E-Mail gesendet:', info.response);
      res.status(200).send('E-Mail erfolgreich gesendet');
    }
  });
});

app.listen(3001, () => {
  console.log('E-Mail-Service läuft auf Port 3001');
});
