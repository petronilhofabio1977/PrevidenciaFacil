export default function AdminFinal() {
  return (
    <html>
      <head>
        <title>Admin - PrevidênciaFácil</title>
      </head>
      <body style={{ margin: 0, padding: 0 }}>
        <div style={{ 
          minHeight: '100vh', 
          background: '#10b981',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'system-ui, -apple-system, sans-serif'
        }}>
          <div style={{
            background: 'white',
            padding: '3rem',
            borderRadius: '1rem',
            textAlign: 'center',
            boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)'
          }}>
            <h1 style={{ fontSize: '3rem', color: '#059669', marginBottom: '1rem' }}>✅</h1>
            <h2 style={{ fontSize: '2rem', color: '#1f2937', marginBottom: '1rem' }}>
              ADMIN FUNCIONOU!
            </h2>
            <p style={{ color: '#6b7280', marginBottom: '2rem' }}>
              Você está na área administrativa
            </p>
            <button
              onclick="localStorage.clear(); window.location.href='/login'"
              style={{
                padding: '0.75rem 1.5rem',
                background: '#dc2626',
                color: 'white',
                border: 'none',
                borderRadius: '0.5rem',
                fontSize: '1rem',
                cursor: 'pointer'
              }}
            >
              Sair
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
