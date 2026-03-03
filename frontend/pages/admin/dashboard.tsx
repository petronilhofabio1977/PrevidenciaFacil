import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../../components/layout/Layout';

export default function AdminDashboard() {
  const router = useRouter();
  const [usuario, setUsuario] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar se usuário está logado e é admin
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('usuario');
    
    if (!token || !userStr) {
      router.push('/login');
      return;
    }

    const user = JSON.parse(userStr);
    setUsuario(user);

    if (!user.is_admin) {
      router.push('/dashboard');
      return;
    }

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
          Painel Administrativo
        </h1>
        <p style={{ marginBottom: '2rem' }}>
          Bem-vindo, {usuario?.nome}!
        </p>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '1rem' 
        }}>
          <div style={{ 
            background: 'white', 
            padding: '1.5rem', 
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ fontWeight: '600', marginBottom: '0.5rem' }}>Escritórios</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2563eb' }}>1</p>
          </div>

          <div style={{ 
            background: 'white', 
            padding: '1.5rem', 
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ fontWeight: '600', marginBottom: '0.5rem' }}>Usuários</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#059669' }}>1</p>
          </div>

          <div style={{ 
            background: 'white', 
            padding: '1.5rem', 
            borderRadius: '0.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ fontWeight: '600', marginBottom: '0.5rem' }}>Clientes</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7c3aed' }}>0</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
