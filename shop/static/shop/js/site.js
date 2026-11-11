// The website works without JavaScript. This file is for progressive enhancement.
document.querySelectorAll('.flash').forEach((notice) => {
  notice.setAttribute('role', 'status');
});
