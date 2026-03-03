import React, { useState } from 'react';
import { Eye, MoreHorizontal, AlertCircle, CheckCircle, XCircle, FileText, Upload, User, Briefcase, Shield } from 'lucide-react';

export default function AnalisePage() {
  const [clienteSelecionado, setClienteSelecionado] = useState('joao');
  
  // Dados mockados dos clientes
  const clientesMock = [
    { id: 'joao', nome: 'João da Silva', cpf: '000.***.***-00', idade: 62, tempoContribuicao: '32 anos, 4 meses' },
    { id: 'maria', nome: 'Maria Oliveira', cpf: '111.***.***-11', idade: 55, tempoContribuicao: '28 anos, 2 meses' },
    { id: 'carlos', nome: 'Carlos Santos', cpf: '222.***.***-22', idade: 58, tempoContribuicao: '30 anos, 8 meses' },
  ];

  // Benefícios com dados mockados
  const beneficios = [
    { nome: 'Aposentadoria por Idade', progresso: 85, status: 'Pronto', acao: 'Ver Pendências', statusClass: 'bg-blue-100 text-blue-700' },
    { nome: 'Aposentadoria Especial', progresso: 30, status: 'Inelegível', acao: 'Ver Por Quê?', statusClass: 'bg-red-100 text-red-700' },
    { nome: 'Aposentadoria por Tempo', progresso: 100, status: 'Disponível', acao: 'Simular RMI', statusClass: 'bg-green-100 text-green-700' },
    { nome: 'Aposentadoria Rural', progresso: 60, status: 'Em análise', acao: 'Ver Pendências', statusClass: 'bg-yellow-100 text-yellow-700' },
    { nome: 'Aposentadoria Professor', progresso: 80, status: 'Pronto', acao: 'Simular RMI', statusClass: 'bg-blue-100 text-blue-700' },
    { nome: 'Pedágio 50%', progresso: 75, status: 'Em análise', acao: 'Ver Pendências', statusClass: 'bg-yellow-100 text-yellow-700' },
    { nome: 'Pedágio 100%', progresso: 70, status: 'Em análise', acao: 'Ver Por Quê?', statusClass: 'bg-yellow-100 text-yellow-700' },
    { nome: 'BPC/LOAS', progresso: 45, status: 'Inelegível', acao: 'Ver Por Quê?', statusClass: 'bg-red-100 text-red-700' },
    { nome: 'Pensão por Morte', progresso: 0, status: 'N/A', acao: '-', statusClass: 'bg-gray-100 text-gray-700' },
    { nome: 'Auxílio-Incapacidade', progresso: 90, status: 'Disponível', acao: 'Simular RMI', statusClass: 'bg-green-100 text-green-700' }
  ];

  const clienteAtual = clientesMock.find(c => c.id === clienteSelecionado) || clientesMock[0];

  // Documentos mockados
  const documentos = [
    { categoria: 'Identidade', icon: <User className="w-5 h-5" />, itens: [
      { nome: 'RG / CNH', status: 'validado' },
      { nome: 'CPF', status: 'validado' },
      { nome: 'Certidão de Nascimento/Casamento', status: 'pendente' }
    ]},
    { categoria: 'Vínculos (CNIS/CTPS)', icon: <Briefcase className="w-5 h-5" />, itens: [
      { nome: 'Extrato CNIS Completo', status: 'pendente' },
      { nome: 'CTPS (Física/Digital)', status: 'invalido', obs: 'Páginas ilegíveis' },
      { nome: 'Carnês de Contribuição', status: 'pendente' }
    ]},
    { categoria: 'Provas Especiais (PPP/LTCAT)', icon: <Shield className="w-5 h-5" />, itens: [
      { nome: 'Perfil Profissiográfico (PPP)', status: 'pendente' },
      { nome: 'Laudo Técnico (LTCAT)', status: 'pendente' },
      { nome: 'Receituário Médico', status: 'validado' }
    ]}
  ];

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'validado': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'pendente': return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'invalido': return <XCircle className="w-5 h-5 text-red-500" />;
      default: return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header do Cliente com Seletor */}
      <div className="bg-white rounded-lg p-4 border border-gray-200 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-gray-700 font-medium">CLIENTE:</span>
          <select 
            className="border border-gray-300 rounded-md px-3 py-1 text-gray-700"
            value={clienteSelecionado}
            onChange={(e) => setClienteSelecionado(e.target.value)}
          >
            {clientesMock.map(c => (
              <option key={c.id} value={c.id}>{c.nome}</option>
            ))}
          </select>
          <span className="text-gray-500">|</span>
          <span className="text-gray-700">CPF: {clienteAtual.cpf}</span>
          <span className="text-gray-500">|</span>
          <span className="text-gray-700">Idade: {clienteAtual.idade} anos</span>
        </div>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
          Atualizar Análise
        </button>
      </div>

      {/* Grid de 2 colunas: Documentos e Cards de Info */}
      <div className="grid grid-cols-3 gap-6">
        {/* Checklist de Documentos (ocupa 2 colunas) */}
        <div className="col-span-2 bg-white rounded-lg border border-gray-200">
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Checklist de Documentos</h2>
          </div>
          <div className="p-4">
            {/* Área de Upload */}
            <div className="border-2 border-dashed rounded-lg p-6 mb-6 text-center border-gray-300 hover:border-blue-400 cursor-pointer">
              <Upload className="w-8 h-8 mx-auto text-gray-400 mb-2" />
              <p className="text-sm text-gray-600">Clique para fazer upload</p>
              <p className="text-xs text-gray-400 mt-1">PDF, JPG ou PNG</p>
            </div>

            {/* Lista de Documentos */}
            <div className="space-y-4">
              {documentos.map((cat, idx) => (
                <div key={idx} className="border rounded-lg overflow-hidden">
                  <div className="bg-gray-50 px-4 py-2 border-b flex items-center gap-2">
                    {cat.icon}
                    <h3 className="font-medium text-gray-700">{cat.categoria}</h3>
                  </div>
                  <div className="divide-y">
                    {cat.itens.map((item, i) => (
                      <div key={i} className="px-4 py-2 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <FileText className="w-4 h-4 text-gray-400" />
                          <span className="text-sm text-gray-600">{item.nome}</span>
                          {item.obs && <span className="text-xs text-gray-400">({item.obs})</span>}
                        </div>
                        {getStatusIcon(item.status)}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Cards de Informação (ocupa 1 coluna) */}
        <div className="space-y-4">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Tempo de Contribuição</h3>
            <p className="text-xl font-semibold text-gray-900">{clienteAtual.tempoContribuicao}</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Qualidade de Segurado</h3>
            <p className="text-xl font-semibold text-green-600">ATIVA (Até 15/05/2027)</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Última Análise</h3>
            <p className="text-sm text-gray-700">27/02/2026 - 10:30</p>
            <p className="text-xs text-gray-500 mt-1">3 regras elegíveis</p>
          </div>
        </div>
      </div>

      {/* Tabela de Elegibilidade */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">TABELA DE ELEGIBILIDADE (10 BENEFÍCIOS)</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Benefício</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Progresso</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Status</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Ação</th>
                <th className="w-10"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {beneficios.map((beneficio, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900">{beneficio.nome}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-gray-200 rounded-full">
                        <div 
                          className="h-2 bg-blue-600 rounded-full"
                          style={{ width: `${beneficio.progresso}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-600">{beneficio.progresso}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${beneficio.statusClass}`}>
                      {beneficio.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    {beneficio.acao !== '-' ? (
                      <button className="text-sm text-blue-600 hover:text-blue-800">
                        {beneficio.acao}
                      </button>
                    ) : (
                      <span className="text-sm text-gray-400">-</span>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <button className="text-gray-400 hover:text-gray-600">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
