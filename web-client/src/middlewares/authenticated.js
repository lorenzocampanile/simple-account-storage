export default function authenticated({ next, router }) {
  if (!sessionStorage.getItem('privateKey')) {
    return router.push({ name: 'login' });
  }

  return next();
}