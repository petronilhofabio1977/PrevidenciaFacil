import React, { useState } from 'react';
import { User, Bell, Shield, Database, Save } from 'lucide-react';

export default function Configuracoes() {
  const [config, setConfig] = useState({
    nome: 'Dra. Ana Paula',
    email: 'ana.paula@escritorio.com',
    oab: '123.456/SP',
    notificacoes: true,
    relatoriosAutomaticos: false,
    tema: 'claro'
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>
        <p className="text-gray-500">Configurações do sistema</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Menu lateral de configurações */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <nav className="space-y-1">
              {[
                { icon: User, nome: 'Perfil' },
                { icon: Bell, nome: 'Notificações' },
                { icon: Shield, nome: 'Segurança' },
                { icon: Database, nome: 'Dados' },
              ].map((item, index) => {
                const Icon = item.icon;
                return (
                  <button
                    key={index}
                    className="w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg hover:bg-gray-50 text-gray-700"
                  >
                    <Icon className="w-5 h-5 text-gray-400" />
                    <span className="font-medium">{item.nome}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Conteúdo das configurações */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">Perfil do Advogado</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome</label>
                <input
                  type="text"
                  value={config.nome}
                  onChange={(e) => setConfig({...config, nome: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={config.email}
                  onChange={(e) => setConfig({...config, email: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">OAB</label>
                <input
                  type="text"
                  value={config.oab}
                  onChange={(e) => setConfig({...config, oab: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="pt-4">
                <h3 className="text-md font-medium text-gray-900 mb-3">Preferências</h3>
                
                <div className="space-y-3">
                  <label className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={config.notificacoes}
                      onChange={(e) => setConfig({...config, notificacoes: e.target.checked})}
                      className="w-4 h-4 text-blue-600 rounded"
                    />
                    <span className="text-sm text-gray-700">Receber notificações por email</span>
                  </label>

                  <label className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={config.relatoriosAutomaticos}
                      onChange={(e) => setConfig({...config, relatoriosAutomaticos: e.target.checked})}
                      className="w-4 h-4 text-blue-600 rounded"
                    />
                    <span className="text-sm text-gray-700">Gerar relatórios automaticamente</span>
                  </label>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Tema</label>
                    <select
                      value={config.tema}
                      onChange={(e) => setConfig({...config, tema: e.target.value})}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="claro">Claro</option>
                      <option value="escuro">Escuro</option>
                      <option value="sistema">Sistema</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="pt-4">
                <button className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  <Save className="w-4 h-4" />
                  Salvar Configurações
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
