# Initial Response

function validateEmail(email) {
  const emailRegEx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegEx.test(email);
}

// Example usage
console.log(validateEmail('example@example.com')); // true
console.log(validateEmail('example@example')); // false