import React from 'react';
import { CheckCircle, AlertCircle, XCircle, HelpCircle } from 'lucide-react';

interface Beneficio {
  id: string;
  nome: string;
  descricao: string;
  progresso: number;
  status: 'elegivel' | 'em_analise' | 'nao_elegivel';
  observacao?: string;
}

export default function MatrizElegibilidade() {
  const beneficios: Beneficio[] = [
    {
      id: 'aposentadoria_idade',
      nome: 'Aposentadoria por Idade',
      descricao: '65 anos (H) / 62 anos (M) + carência',
      progresso: 85,
      status: 'em_analise',
      observacao: 'Quase atingiu, faltam 2 anos'
    },
    {
      id: 'aposentadoria_tempo',
      nome: 'Aposentadoria por Tempo de Contribuição',
      descricao: '35 anos (H) / 30 anos (M)',
      progresso: 100,
      status: 'elegivel',
      observacao: 'Direito adquirido'
    },
    {
      id: 'aposentadoria_pontos',
      nome: 'Regra de Pontos',
      descricao: 'Idade + Tempo de Contribuição',
      progresso: 92,
      status: 'elegivel'
    },
    {
      id: 'aposentadoria_pedagio50',
      nome: 'Pedágio 50%',
      descricao: '50% do tempo que faltava em 2019',
      progresso: 65,
      status: 'em_analise',
      observacao: 'Faltam 3 anos'
    },
    {
      id: 'aposentadoria_pedagio100',
      nome: 'Pedágio 100%',
      descricao: '100% do tempo que faltava + idade mínima',
      progresso: 70,
      status: 'em_analise'
    },
    {
      id: 'aposentadoria_especial',
      nome: 'Aposentadoria Especial',
      descricao: '15/20/25 anos em atividade especial',
      progresso: 45,
      status: 'nao_elegivel',
      observacao: 'Documentação incompleta'
    },
    {
      id: 'aposentadoria_professor',
      nome: 'Aposentadoria de Professor',
      descricao: 'Redução de 5 anos nos requisitos',
      progresso: 100,
      status: 'elegivel'
    },
    {
      id: 'aposentadoria_rural',
      nome: 'Aposentadoria Rural',
      descricao: '60 anos (H) / 55 anos (M)',
      progresso: 30,
      status: 'nao_elegivel',
      observacao: 'Comprovação rural insuficiente'
    },
    {
      id: 'aposentadoria_deficiente',
      nome: 'Aposentadoria da Pessoa com Deficiência',
      descricao: '20/24/28 anos conforme grau',
      progresso: 80,
      status: 'em_analise'
    },
    {
      id: 'bpc_loas',
      nome: 'BPC/LOAS',
      descricao: 'Benefício de Prestação Continuada',
      progresso: 50,
      status: 'em_analise'
    }
  ];

  const getStatusBadge = (status: string) => {
    switch(status) {
      case 'elegivel':
        return {
          icon: <CheckCircle className="w-4 h-4 text-green-500" />,
          text: 'Elegível',
          class: 'bg-green-100 text-green-800'
        };
      case 'em_analise':
        return {
          icon: <AlertCircle className="w-4 h-4 text-yellow-500" />,
          text: 'Em análise',
          class: 'bg-yellow-100 text-yellow-800'
        };
      case 'nao_elegivel':
        return {
          icon: <XCircle className="w-4 h-4 text-red-500" />,
          text: 'Não elegível',
          class: 'bg-red-100 text-red-800'
        };
      default:
        return {
          icon: <HelpCircle className="w-4 h-4 text-gray-500" />,
          text: 'Indefinido',
          class: 'bg-gray-100 text-gray-800'
        };
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Matriz de Elegibilidade</h2>
        <p className="text-sm text-gray-500 mt-1">Análise dos 10 benefícios previdenciários</p>
      </div>

      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {beneficios.map((beneficio) => {
            const badge = getStatusBadge(beneficio.status);
            return (
              <div key={beneficio.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-medium text-gray-900">{beneficio.nome}</h3>
                    <p className="text-xs text-gray-500 mt-1">{beneficio.descricao}</p>
                  </div>
                  <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${badge.class}`}>
                    {badge.icon}
                    {badge.text}
                  </span>
                </div>

                {/* Barra de Progresso */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-500">Requisitos atingidos</span>
                    <span className="font-medium text-gray-700">{beneficio.progresso}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        beneficio.progresso >= 100 ? 'bg-green-500' :
                        beneficio.progresso >= 70 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${Math.min(beneficio.progresso, 100)}%` }}
                    />
                  </div>
                </div>

                {beneficio.observacao && (
                  <p className="text-xs text-gray-500 mt-3 italic">{beneficio.observacao}</p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
