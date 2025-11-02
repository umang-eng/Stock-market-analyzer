/**
 * AI Market Insights - Client-Side Authentication & User Management
 * Secure Firebase integration for user personalization
 */

// Initialize Firebase (assumes Firebase SDK is loaded)
// const { initializeApp } = require('firebase/app');
// const { getAuth, GoogleAuthProvider } = require('firebase/auth');
// const { getFirestore, serverTimestamp } = require('firebase/firestore');

// Firebase configuration (replace with your config)
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Google Auth Provider
const googleProvider = new GoogleAuthProvider();
googleProvider.addScope('email');
googleProvider.addScope('profile');

/**
 * Authentication Management
 */

/**
 * Initialize authentication state listener
 * @param {Function} onLogin - Callback when user signs in
 * @param {Function} onLogout - Callback when user signs out
 */
function initializeAuth(onLogin, onLogout) {
  auth.onAuthStateChanged((user) => {
    if (user) {
      console.log('User signed in:', user.uid);
      onLogin(user);
    } else {
      console.log('User signed out');
      onLogout();
    }
  });
}

/**
 * Sign in with Google
 * @returns {Promise<User>} User object on success
 */
async function signInWithGoogle() {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;
    
    console.log('Google sign-in successful:', user.uid);
    
    // Optional: Create user document in Firestore
    await createUserDocument(user);
    
    return user;
  } catch (error) {
    console.error('Google sign-in error:', error);
    throw error;
  }
}

/**
 * Sign out the current user
 */
async function signOutUser() {
  try {
    await auth.signOut();
    console.log('User signed out successfully');
  } catch (error) {
    console.error('Sign-out error:', error);
    throw error;
  }
}

/**
 * Create user document in Firestore (optional)
 * @param {User} user - Firebase user object
 */
async function createUserDocument(user) {
  try {
    const userRef = doc(db, 'users', user.uid);
    const userDoc = await getDoc(userRef);
    
    if (!userDoc.exists()) {
      await setDoc(userRef, {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
        createdAt: serverTimestamp(),
        lastLoginAt: serverTimestamp()
      });
      console.log('User document created');
    } else {
      // Update last login time
      await updateDoc(userRef, {
        lastLoginAt: serverTimestamp()
      });
    }
  } catch (error) {
    console.error('Error creating user document:', error);
  }
}

/**
 * Watchlist Management
 */

/**
 * Get user's watchlist with real-time updates
 * @param {string} userId - User's UID
 * @param {Function} callback - Callback function to receive watchlist data
 * @returns {Function} Unsubscribe function
 */
function getWatchlist(userId, callback) {
  const watchlistRef = collection(db, 'users', userId, 'watchlist');
  
  const unsubscribe = onSnapshot(watchlistRef, (snapshot) => {
    const watchlist = [];
    snapshot.forEach((doc) => {
      watchlist.push({
        id: doc.id,
        ...doc.data()
      });
    });
    
    console.log('Watchlist updated:', watchlist);
    callback(watchlist);
  }, (error) => {
    console.error('Error getting watchlist:', error);
    callback([]);
  });
  
  return unsubscribe;
}

/**
 * Add stock to user's watchlist
 * @param {string} userId - User's UID
 * @param {string} tickerSymbol - Stock ticker symbol (e.g., 'RELIANCE')
 * @param {Object} stockData - Additional stock data (optional)
 * @returns {Promise<string>} Document ID of the added stock
 */
async function addToWatchlist(userId, tickerSymbol, stockData = {}) {
  try {
    // Check if ticker already exists
    const watchlistRef = collection(db, 'users', userId, 'watchlist');
    const q = query(watchlistRef, where('ticker', '==', tickerSymbol));
    const existingDocs = await getDocs(q);
    
    if (!existingDocs.empty) {
      throw new Error('Stock already in watchlist');
    }
    
    // Add to watchlist
    const docRef = await addDoc(watchlistRef, {
      ticker: tickerSymbol.toUpperCase(),
      addedAt: serverTimestamp(),
      ...stockData
    });
    
    console.log('Stock added to watchlist:', tickerSymbol);
    return docRef.id;
  } catch (error) {
    console.error('Error adding to watchlist:', error);
    throw error;
  }
}

/**
 * Remove stock from user's watchlist
 * @param {string} userId - User's UID
 * @param {string} tickerDocId - Document ID of the watchlist item
 */
async function removeFromWatchlist(userId, tickerDocId) {
  try {
    const docRef = doc(db, 'users', userId, 'watchlist', tickerDocId);
    await deleteDoc(docRef);
    
    console.log('Stock removed from watchlist:', tickerDocId);
  } catch (error) {
    console.error('Error removing from watchlist:', error);
    throw error;
  }
}

/**
 * Update watchlist item (e.g., add notes, alerts)
 * @param {string} userId - User's UID
 * @param {string} tickerDocId - Document ID of the watchlist item
 * @param {Object} updateData - Data to update
 */
async function updateWatchlistItem(userId, tickerDocId, updateData) {
  try {
    const docRef = doc(db, 'users', userId, 'watchlist', tickerDocId);
    await updateDoc(docRef, {
      ...updateData,
      updatedAt: serverTimestamp()
    });
    
    console.log('Watchlist item updated:', tickerDocId);
  } catch (error) {
    console.error('Error updating watchlist item:', error);
    throw error;
  }
}

/**
 * Feedback Management
 */

/**
 * Submit user feedback
 * @param {string} userId - User's UID
 * @param {Object} feedbackData - Feedback data
 * @returns {Promise<string>} Document ID of the submitted feedback
 */
async function submitFeedback(userId, feedbackData) {
  try {
    const feedbackRef = collection(db, 'feedback');
    
    const docRef = await addDoc(feedbackRef, {
      userId: userId,
      submittedAt: serverTimestamp(),
      ...feedbackData
    });
    
    console.log('Feedback submitted:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('Error submitting feedback:', error);
    throw error;
  }
}

/**
 * User Preferences Management
 */

/**
 * Get user preferences
 * @param {string} userId - User's UID
 * @param {Function} callback - Callback function to receive preferences
 * @returns {Function} Unsubscribe function
 */
function getUserPreferences(userId, callback) {
  const prefsRef = collection(db, 'users', userId, 'preferences');
  
  const unsubscribe = onSnapshot(prefsRef, (snapshot) => {
    const preferences = {};
    snapshot.forEach((doc) => {
      preferences[doc.id] = doc.data();
    });
    
    callback(preferences);
  }, (error) => {
    console.error('Error getting preferences:', error);
    callback({});
  });
  
  return unsubscribe;
}

/**
 * Update user preferences
 * @param {string} userId - User's UID
 * @param {string} preferenceKey - Preference key
 * @param {Object} preferenceData - Preference data
 */
async function updateUserPreferences(userId, preferenceKey, preferenceData) {
  try {
    const docRef = doc(db, 'users', userId, 'preferences', preferenceKey);
    await setDoc(docRef, {
      ...preferenceData,
      updatedAt: serverTimestamp()
    }, { merge: true });
    
    console.log('Preferences updated:', preferenceKey);
  } catch (error) {
    console.error('Error updating preferences:', error);
    throw error;
  }
}

/**
 * Utility Functions
 */

/**
 * Get current user
 * @returns {User|null} Current user or null
 */
function getCurrentUser() {
  return auth.currentUser;
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if user is authenticated
 */
function isAuthenticated() {
  return auth.currentUser !== null;
}

/**
 * Get user's UID
 * @returns {string|null} User's UID or null
 */
function getCurrentUserId() {
  return auth.currentUser?.uid || null;
}

/**
 * Error handling utility
 * @param {Error} error - Error object
 * @returns {string} User-friendly error message
 */
function getErrorMessage(error) {
  const errorMessages = {
    'auth/user-not-found': 'User not found',
    'auth/wrong-password': 'Incorrect password',
    'auth/email-already-in-use': 'Email already in use',
    'auth/weak-password': 'Password is too weak',
    'auth/network-request-failed': 'Network error. Please check your connection',
    'permission-denied': 'You do not have permission to perform this action',
    'unavailable': 'Service temporarily unavailable'
  };
  
  return errorMessages[error.code] || error.message || 'An unexpected error occurred';
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    initializeAuth,
    signInWithGoogle,
    signOutUser,
    getWatchlist,
    addToWatchlist,
    removeFromWatchlist,
    updateWatchlistItem,
    submitFeedback,
    getUserPreferences,
    updateUserPreferences,
    getCurrentUser,
    isAuthenticated,
    getCurrentUserId,
    getErrorMessage
  };
}
