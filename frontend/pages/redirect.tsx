import { useEffect } from 'react';

export default function RedirectPage() {
  useEffect(() => {
    // Verificar se está logado
    const token = localStorage.getItem('token');
    const usuario = localStorage.getItem('usuario');
    
    console.log('🔍 RedirectPage - Token:', token);
    console.log('🔍 RedirectPage - Usuário:', usuario);
    
    if (!token) {
      window.location.href = '/login';
      return;
    }
    
    const userData = JSON.parse(usuario || '{}');
    
    if (userData.is_admin) {
      window.location.href = '/admin-final';
    } else {
      window.location.href = '/dashboard';
    }
  }, []);

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      fontFamily: 'system-ui, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h2>Redirecionando...</h2>
        <p>Por favor, aguarde.</p>
      </div>
    </div>
  );
}
