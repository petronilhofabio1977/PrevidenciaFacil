import React from 'react';
import { Clock, FileText, Download, Eye } from 'lucide-react';

export default function Historico() {
  const historico = [
    { data: '27/02/2026 14:30', cliente: 'João da Silva', tipo: 'Análise Completa', regras: 10, elegiveis: 3, arquivo: 'relatorio_joao_2702.pdf' },
    { data: '26/02/2026 10:15', cliente: 'Maria Oliveira', tipo: 'Análise Parcial', regras: 5, elegiveis: 2, arquivo: 'relatorio_maria_2602.pdf' },
    { data: '26/02/2026 09:30', cliente: 'Carlos Santos', tipo: 'Análise Completa', regras: 10, elegiveis: 5, arquivo: 'relatorio_carlos_2602.pdf' },
    { data: '25/02/2026 16:45', cliente: 'Ana Paula', tipo: 'Simulação', regras: 3, elegiveis: 1, arquivo: 'simulacao_ana_2502.pdf' },
    { data: '24/02/2026 11:20', cliente: 'Pedro Costa', tipo: 'Análise Completa', regras: 10, elegiveis: 4, arquivo: 'relatorio_pedro_2402.pdf' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Histórico</h1>
        <p className="text-gray-500">Histórico de análises realizadas</p>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Data/Hora</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Cliente</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Tipo</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Regras</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Elegíveis</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {historico.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-600">{item.data}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">{item.cliente}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{item.tipo}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{item.regras}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                    {item.elegiveis} elegíveis
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <Eye className="w-4 h-4 text-gray-500" />
                    </button>
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <Download className="w-4 h-4 text-gray-500" />
                    </button>
                    <button className="p-1 hover:bg-gray-100 rounded">
                      <FileText className="w-4 h-4 text-gray-500" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
