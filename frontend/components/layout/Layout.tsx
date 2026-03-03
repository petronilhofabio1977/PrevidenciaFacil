import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  LayoutDashboard, 
  FileText, 
  Calculator, 
  History, 
  Settings,
  Search,
  ChevronDown,
  BarChart3
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const menuItems = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Documentos', href: '/documentos', icon: FileText },
  { name: 'Cálculos', href: '/calculos', icon: Calculator },
  { name: 'Análise', href: '/analise', icon: BarChart3 },
  { name: 'Histórico', href: '/historico', icon: History },
  { name: 'Configurações', href: '/configuracoes', icon: Settings },
];

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();

  // Para debug - verificar rota atual
  console.log('Rota atual:', router.pathname);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header Superior */}
      <header className="bg-white border-b border-gray-200 fixed top-0 left-0 right-0 z-10">
        <div className="flex items-center justify-between h-16 px-6">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">PF</span>
            </div>
            <span className="text-xl font-bold text-gray-900">PrevidenciaFacil</span>
          </div>

          {/* Busca de Clientes */}
          <div className="flex-1 max-w-md mx-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Buscar cliente por nome ou CPF..."
                className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Perfil do Advogado */}
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">Dra. Ana Paula</p>
              <p className="text-xs text-gray-500">OAB/SP 123.456</p>
            </div>
            <button className="flex items-center gap-1 px-2 py-1 hover:bg-gray-50 rounded-lg">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">AP</span>
              </div>
              <ChevronDown className="w-4 h-4 text-gray-500" />
            </button>
          </div>
        </div>
      </header>

      {/* Menu Lateral e Conteúdo */}
      <div className="flex pt-16">
        {/* Menu Lateral */}
        <aside className="w-64 bg-white border-r border-gray-200 fixed left-0 top-16 bottom-0 overflow-y-auto">
          <nav className="p-4">
            {menuItems.map((item) => {
              const isActive = router.pathname === item.href;
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center gap-3 px-4 py-3 mb-1 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'text-blue-600' : 'text-gray-400'}`} />
                  <span className="font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Versão do sistema */}
          <div className="absolute bottom-4 left-0 right-0 px-4">
            <p className="text-xs text-gray-400 text-center">Versão 1.0.0</p>
          </div>
        </aside>

        {/* Conteúdo Principal */}
        <main className="flex-1 ml-64 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
