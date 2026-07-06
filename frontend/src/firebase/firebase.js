// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB1HTxwAVnZklWmdkmy_S0Q-BURgs3yJ9c",
  authDomain: "ticketing-29354.firebaseapp.com",
  projectId: "ticketing-29354",
  storageBucket: "ticketing-29354.firebasestorage.app",
  messagingSenderId: "153611573064",
  appId: "1:153611573064:web:c62124aaaa682e69b5457d"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { app, auth, googleProvider };