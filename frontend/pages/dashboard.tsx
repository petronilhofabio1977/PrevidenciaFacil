import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/layout/Layout';

export default function Dashboard() {
  const router = useRouter();
  const [usuario, setUsuario] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('usuario');
    
    if (!token || !userStr) {
      router.push('/login');
      return;
    }

    setUsuario(JSON.parse(userStr));
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center' 
      }}>
        <p>Carregando...</p>
      </div>
    );
  }

  return (
    <Layout>
      <div style={{ padding: '2rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem' }}>
          Dashboard
        </h1>
        <p>Bem-vindo, {usuario?.nome}!</p>
      </div>
    </Layout>
  );
}
