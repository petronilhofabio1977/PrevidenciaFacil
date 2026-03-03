import React, { useState } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('petronilho@email.com');
  const [senha, setSenha] = useState('6121060F1977po!');
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErro('');

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password: senha })
      });

      const data = await response.json();

      if (response.ok && data.access_token) {
        // Salva no localStorage (para uso no frontend)
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('usuario', JSON.stringify(data.usuario));

        // Salva no cookie (para o middleware do Next.js conseguir ler)
        document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;

        // Redireciona
        if (data.usuario?.is_admin) {
          window.location.href = '/admin-final';
        } else {
          window.location.href = '/dashboard';
        }
      } else {
        setErro(data.detail || 'Email ou senha inválidos');
      }
    } catch (error: any) {
      setErro('Erro de conexão: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{
        background: 'white',
        padding: '2.5rem',
        borderRadius: '1rem',
        width: '100%',
        maxWidth: '400px',
        boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 'bold',
          marginBottom: '2rem',
          textAlign: 'center',
          color: '#1f2937'
        }}>
          PrevidênciaFácil
        </h1>

        {erro && (
          <div style={{
            backgroundColor: '#fee2e2',
            color: '#dc2626',
            padding: '0.75rem',
            borderRadius: '0.5rem',
            marginBottom: '1rem',
            fontSize: '0.875rem',
            border: '1px solid #fecaca'
          }}>
            {erro}
          </div>
        )}

        <form onSubmit={handleLogin}>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: '100%', padding: '0.75rem', marginBottom: '1rem',
              border: '1px solid #d1d5db', borderRadius: '0.5rem',
              fontSize: '1rem', boxSizing: 'border-box'
            }}
            placeholder="Email"
            required
          />
          <input
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            style={{
              width: '100%', padding: '0.75rem', marginBottom: '1.5rem',
              border: '1px solid #d1d5db', borderRadius: '0.5rem',
              fontSize: '1rem', boxSizing: 'border-box'
            }}
            placeholder="Senha"
            required
          />
          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%', padding: '0.75rem',
              background: '#2563eb', color: 'white',
              border: 'none', borderRadius: '0.5rem',
              fontSize: '1rem', fontWeight: '500',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1
            }}
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  );
}
