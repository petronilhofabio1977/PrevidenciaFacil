import React, { useState } from 'react';
import { CheckCircle, AlertCircle, XCircle, Upload, FileText, Shield, User, Briefcase } from 'lucide-react';

interface Documento {
  id: string;
  nome: string;
  status: 'validado' | 'pendente' | 'invalido';
  observacao?: string;
}

interface CategoriaDocumento {
  id: string;
  titulo: string;
  icon: React.ReactNode;
  documentos: Documento[];
}

export default function DocumentChecklist() {
  const [documentos] = useState<CategoriaDocumento[]>([
    {
      id: 'identidade',
      titulo: 'Identidade',
      icon: <User className="w-5 h-5" />,
      documentos: [
        { id: 'rg', nome: 'RG / CNH', status: 'validado' },
        { id: 'cpf', nome: 'CPF', status: 'validado' },
        { id: 'certidao', nome: 'Certidão de Nascimento/Casamento', status: 'pendente' }
      ]
    },
    {
      id: 'vinculos',
      titulo: 'Vínculos (CNIS/CTPS)',
      icon: <Briefcase className="w-5 h-5" />,
      documentos: [
        { id: 'cnis', nome: 'Extrato CNIS Completo', status: 'pendente' },
        { id: 'ctps', nome: 'CTPS (Física/Digital)', status: 'invalido', observacao: 'Páginas ilegíveis' },
        { id: 'carnes', nome: 'Carnês de Contribuição', status: 'pendente' }
      ]
    },
    {
      id: 'especiais',
      titulo: 'Provas Especiais (PPP/LTCAT)',
      icon: <Shield className="w-5 h-5" />,
      documentos: [
        { id: 'ppp', nome: 'Perfil Profissiográfico (PPP)', status: 'pendente' },
        { id: 'ltcat', nome: 'Laudo Técnico (LTCAT)', status: 'pendente' },
        { id: 'receituario', nome: 'Receituário Médico', status: 'validado' }
      ]
    }
  ]);

  // Versão simplificada sem o useDropzone por enquanto
  const handleUploadClick = () => {
    alert('Funcionalidade de upload será implementada em breve!');
  };

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'validado':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'pendente':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'invalido':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return null;
    }
  };

  const getStatusText = (status: string) => {
    switch(status) {
      case 'validado': return 'Validado';
      case 'pendente': return 'Pendente';
      case 'invalido': return 'Inválido';
      default: return '';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Checklist de Documentos</h2>
        <p className="text-sm text-gray-500 mt-1">Acompanhe o status dos documentos do cliente</p>
      </div>

      <div className="p-6">
        {/* Área de Upload simplificada */}
        <div 
          onClick={handleUploadClick}
          className="border-2 border-dashed rounded-lg p-8 mb-8 text-center cursor-pointer hover:border-blue-400 transition-colors border-gray-300"
        >
          <Upload className="w-12 h-12 mx-auto text-gray-400 mb-3" />
          <p className="text-gray-700 font-medium">Clique para fazer upload</p>
          <p className="text-sm text-gray-500 mt-1">PDF, JPG ou PNG (máx. 10MB)</p>
        </div>

        {/* Lista de Documentos por Categoria */}
        <div className="space-y-6">
          {documentos.map((categoria) => (
            <div key={categoria.id} className="border rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-4 py-3 border-b flex items-center gap-2">
                <span className="text-gray-700">{categoria.icon}</span>
                <h3 className="font-medium text-gray-900">{categoria.titulo}</h3>
              </div>
              <div className="divide-y">
                {categoria.documentos.map((doc) => (
                  <div key={doc.id} className="px-4 py-3 flex items-center justify-between hover:bg-gray-50">
                    <div className="flex items-center gap-3">
                      <FileText className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-700">{doc.nome}</span>
                      {doc.observacao && (
                        <span className="text-xs text-gray-500">({doc.observacao})</span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(doc.status)}
                      <span className={`text-xs font-medium ${
                        doc.status === 'validado' ? 'text-green-600' :
                        doc.status === 'pendente' ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {getStatusText(doc.status)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
