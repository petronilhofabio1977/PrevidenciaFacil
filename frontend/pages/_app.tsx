import type { AppProps } from 'next/app';
import Layout from '../components/layout/Layout';
import { useRouter } from 'next/router';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();
  
  // Rotas que NÃO devem usar o Layout
  const noLayoutRoutes = ['/login', '/recuperar-senha', '/admin-final', '/teste-redirect'];
  const isNoLayoutRoute = noLayoutRoutes.includes(router.pathname);
  
  if (isNoLayoutRoute) {
    return <Component {...pageProps} />;
  }

  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}
