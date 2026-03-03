import React from 'react';
import { Calculator, TrendingUp, DollarSign, Clock } from 'lucide-react';

export default function Calculos() {
  const calculadoras = [
    { nome: 'Fator Previdenciário', desc: 'Calcule o fator previdenciário', icon: TrendingUp },
    { nome: 'RMI Estimada', desc: 'Simule o valor do benefício', icon: DollarSign },
    { nome: 'Tempo de Contribuição', desc: 'Calcule tempo total', icon: Clock },
    { nome: 'Projeção Futura', desc: 'Projete cenários futuros', icon: TrendingUp },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Cálculos</h1>
        <p className="text-gray-500">Calculadoras previdenciárias</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {calculadoras.map((calc, index) => {
          const Icon = calc.icon;
          return (
            <div key={index} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow cursor-pointer">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Icon className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{calc.nome}</h3>
                  <p className="text-sm text-gray-500">{calc.desc}</p>
                </div>
              </div>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Calcular
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
