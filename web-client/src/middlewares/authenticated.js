export default function authenticated({ next, router }) {
  console.log('** ehi', !sessionStorage.getItem('encryptionKey'));
  if (!sessionStorage.getItem('encryptionKey')) {
    return router.push({ name: 'login' });
  }

  return next();
}