# Firebase Security Rules & User Management

## Overview
Complete security configuration and client-side functions for user authentication, personalization, and data protection in the AI Market Insights application.

## Files Included

### 1. `firestore.rules`
Comprehensive security rules for Firestore database with:
- **Default deny**: All access denied by default
- **Public read-only**: Articles, market data, sentiment history
- **User-specific**: Secure access to personal data
- **Feedback system**: Create-only for authenticated users
- **Admin controls**: Future administrative functions

### 2. `client-side-auth.js`
Complete JavaScript module with:
- **Authentication**: Google Sign-In, state management
- **Watchlist**: Real-time updates, add/remove stocks
- **Feedback**: Secure submission system
- **Preferences**: User settings management
- **Error handling**: User-friendly error messages

### 3. `example-integration.html`
Working example showing:
- **Firebase integration**: Complete setup
- **UI components**: Authentication, watchlist, feedback
- **Real-time updates**: Live watchlist synchronization
- **Error handling**: User feedback and validation

## Security Features

### Database Security Rules

#### Public Collections (Read-Only)
```javascript
// Articles, market data, sentiment history
allow read: if true;
allow write: if false;  // Serverless functions only
```

#### User-Specific Collections
```javascript
// Users can only access their own data
allow read, write: if request.auth != null && request.auth.uid == userId;
```

#### Feedback Collection
```javascript
// Create-only for authenticated users
allow create: if request.auth != null;
allow read, update, delete: if false;  // Privacy protection
```

### Authentication Security
- **Google OAuth**: Secure sign-in with Google
- **Token validation**: Firebase handles token verification
- **Session management**: Automatic token refresh
- **Sign-out**: Complete session termination

### Data Privacy
- **User isolation**: Users can only access their own data
- **Feedback privacy**: No read access to submitted feedback
- **Admin separation**: Administrative functions isolated
- **Audit trail**: Server timestamps for all operations

## Database Structure

### Collections Overview
```
firestore/
├── articles/                    # Public read-only
├── market_data_cache/           # Public read-only
├── sentiment_history/           # Public read-only
├── users/
│   └── {userId}/
│       ├── watchlist/           # User-specific
│       ├── preferences/         # User-specific
│       └── activity/           # User-specific
├── feedback/                   # Create-only
├── admin/                      # Admin-only
├── system/                     # Serverless-only
└── analytics/                 # Create-only
```

### Document Schemas

#### User Document
```javascript
{
  uid: string,
  email: string,
  displayName: string,
  photoURL: string,
  createdAt: timestamp,
  lastLoginAt: timestamp
}
```

#### Watchlist Item
```javascript
{
  ticker: string,        // e.g., "RELIANCE"
  addedAt: timestamp,
  notes?: string,       // Optional user notes
  alerts?: object       // Optional price alerts
}
```

#### Feedback Document
```javascript
{
  userId: string,
  category: string,     // "bug", "feature", "general"
  message: string,
  submittedAt: timestamp
}
```

## Setup Instructions

### 1. Firebase Project Setup
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize project
firebase init firestore
```

### 2. Deploy Security Rules
```bash
# Deploy rules to Firebase
firebase deploy --only firestore:rules
```

### 3. Configure Authentication
1. Enable Google Sign-In in Firebase Console
2. Add your domain to authorized domains
3. Configure OAuth consent screen

### 4. Frontend Integration
```html
<!-- Include Firebase SDK -->
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>

<!-- Include your auth module -->
<script src="client-side-auth.js"></script>
```

## API Reference

### Authentication Functions

#### `initializeAuth(onLogin, onLogout)`
Sets up authentication state listener.
```javascript
initializeAuth(
  (user) => console.log('User signed in:', user.uid),
  () => console.log('User signed out')
);
```

#### `signInWithGoogle()`
Triggers Google Sign-In popup.
```javascript
try {
  const user = await signInWithGoogle();
  console.log('Signed in:', user.email);
} catch (error) {
  console.error('Sign-in failed:', error);
}
```

#### `signOutUser()`
Signs out the current user.
```javascript
await signOutUser();
```

### Watchlist Functions

#### `getWatchlist(userId, callback)`
Real-time watchlist updates.
```javascript
const unsubscribe = getWatchlist(userId, (watchlist) => {
  console.log('Watchlist updated:', watchlist);
});
// Later: unsubscribe();
```

#### `addToWatchlist(userId, tickerSymbol)`
Adds stock to watchlist.
```javascript
try {
  const docId = await addToWatchlist(userId, 'RELIANCE');
  console.log('Added with ID:', docId);
} catch (error) {
  console.error('Add failed:', error);
}
```

#### `removeFromWatchlist(userId, tickerDocId)`
Removes stock from watchlist.
```javascript
await removeFromWatchlist(userId, docId);
```

### Feedback Functions

#### `submitFeedback(userId, feedbackData)`
Submits user feedback.
```javascript
const feedbackData = {
  category: 'bug',
  message: 'Found an issue with...'
};
await submitFeedback(userId, feedbackData);
```

## Testing

### Local Testing
1. Open `example-integration.html` in browser
2. Configure Firebase settings
3. Test authentication and watchlist functions

### Security Testing
```bash
# Test rules with Firebase emulator
firebase emulators:start --only firestore

# Run security tests
firebase emulators:exec --only firestore "npm test"
```

### Production Testing
1. Deploy rules to staging environment
2. Test with real user accounts
3. Verify data isolation
4. Check error handling

## Monitoring & Analytics

### Cloud Logging
Monitor authentication events:
```bash
gcloud logging read "resource.type=firebase_auth"
```

### Firestore Usage
Track database operations:
```bash
gcloud logging read "resource.type=firestore_database"
```

### Security Events
Monitor rule violations:
```bash
gcloud logging read "severity>=WARNING AND resource.type=firestore_database"
```

## Best Practices

### Security
- **Principle of least privilege**: Users only access their data
- **Input validation**: Validate all user inputs
- **Error handling**: Don't expose sensitive information
- **Regular audits**: Review security rules periodically

### Performance
- **Real-time listeners**: Unsubscribe when not needed
- **Batch operations**: Group multiple writes
- **Caching**: Cache frequently accessed data
- **Pagination**: Limit query results

### User Experience
- **Loading states**: Show progress indicators
- **Error messages**: Provide clear feedback
- **Offline support**: Handle network issues
- **Accessibility**: Support screen readers

## Troubleshooting

### Common Issues

1. **"Permission denied" errors**
   - Check user authentication status
   - Verify security rules
   - Ensure correct document paths

2. **"User not authenticated"**
   - Check Firebase Auth configuration
   - Verify Google OAuth setup
   - Check domain authorization

3. **"Document not found"**
   - Verify document exists
   - Check collection/document IDs
   - Ensure proper permissions

4. **Real-time updates not working**
   - Check network connection
   - Verify listener setup
   - Check for JavaScript errors

### Debug Mode
Enable debug logging:
```javascript
firebase.firestore.setLogLevel('debug');
```

## Support
For security issues or questions:
1. Check Firebase documentation
2. Review security rules syntax
3. Test with Firebase emulator
4. Contact development team

## Security Considerations

### Data Protection
- All user data is encrypted in transit and at rest
- Personal information is never logged
- Feedback submissions are private
- Admin access is strictly controlled

### Compliance
- GDPR compliance for EU users
- Data retention policies
- User data export/deletion
- Privacy policy adherence

### Incident Response
- Security monitoring alerts
- Automated threat detection
- Incident response procedures
- User notification protocols
