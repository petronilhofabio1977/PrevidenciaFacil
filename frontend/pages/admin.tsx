import React, { useEffect, useState } from 'react';

export default function AdminPage() {
  const [usuario, setUsuario] = useState<any>(null);

  useEffect(() => {
    // Verificar se está logado
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('usuario');
    
    if (!token || !userStr) {
      window.location.replace('/login');
      return;
    }

    const user = JSON.parse(userStr);
    setUsuario(user);

    if (!user.is_admin) {
      window.location.replace('/dashboard');
    }
  }, []);

  if (!usuario) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center' 
      }}>
        Carregando...
      </div>
    );
  }

  return (
    <div style={{ 
      padding: '2rem',
      background: '#f3f4f6',
      minHeight: '100vh'
    }}>
      <h1 style={{ fontSize: '2rem', color: '#1e3a8a', marginBottom: '1rem' }}>
        Painel Administrativo
      </h1>
      <p>Bem-vindo, {usuario.nome}!</p>
      <p>Email: {usuario.email}</p>
      <p>Admin: {usuario.is_admin ? 'Sim' : 'Não'}</p>
      
      <button 
        onClick={() => {
          localStorage.clear();
          window.location.replace('/login');
        }}
        style={{
          padding: '0.5rem 1rem',
          background: '#dc2626',
          color: 'white',
          border: 'none',
          borderRadius: '0.5rem',
          cursor: 'pointer',
          marginTop: '1rem'
        }}
      >
        Sair
      </button>
    </div>
  );
}
