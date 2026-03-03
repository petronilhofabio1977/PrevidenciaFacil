import React, { useState, useEffect } from 'react';
import { FileText, Upload, Download, Eye, CheckCircle, AlertCircle, XCircle, RefreshCw, Trash2 } from 'lucide-react';
import { useDocumentos } from '../hooks/useDocumentos';
import { clientesAPI, Cliente } from '../services/clientes';
import { documentosAPI } from '../services/documentos';

export default function DocumentosPage() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [clienteSelecionado, setClienteSelecionado] = useState<string>('');
  const [uploading, setUploading] = useState(false);
  const [validando, setValidando] = useState<string | null>(null);

  const { documentos, dashboard, loading, error, uploadDocumento, refresh } = useDocumentos(clienteSelecionado);

  useEffect(() => {
    carregarClientes();
  }, []);

  const carregarClientes = async () => {
    try {
      const data = await clientesAPI.listar();
      setClientes(data);
      if (data.length > 0 && !clienteSelecionado) {
        setClienteSelecionado(data[0].id);
      }
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    }
  };

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !clienteSelecionado) return;

    setUploading(true);
    try {
      const result = await uploadDocumento(clienteSelecionado, 'cnis', file);
      alert(result.mensagem);
      if (result.sugestao_cadastro) {
        if (confirm('Dados extraídos! Deseja atualizar o cadastro?')) {
          await documentosAPI.atualizarCadastro(clienteSelecionado, result.id);
          alert('Cadastro atualizado!');
        }
      }
    } catch (error) {
      alert('Erro no upload');
    } finally {
      setUploading(false);
    }
  };

  const handleValidar = async (documentoId: string, status: string) => {
    setValidando(documentoId);
    try {
      await documentosAPI.validarManual(documentoId, status);
      alert(`Documento ${status === 'validado' ? 'validado' : 'rejeitado'} com sucesso!`);
      refresh();
    } catch (error) {
      alert('Erro ao validar documento');
    } finally {
      setValidando(null);
    }
  };

  const handleVisualizar = (documento: any) => {
    // Aqui você pode abrir o documento em uma nova aba
    // Por enquanto, vamos apenas mostrar os dados
    alert(JSON.stringify(documento, null, 2));
  };

  const handleDownload = async (documento: any) => {
    try {
      // Implementar download do arquivo
      alert('Função de download será implementada em breve');
    } catch (error) {
      alert('Erro ao baixar documento');
    }
  };

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'validado': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'pendente': return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'invalido': return <XCircle className="w-5 h-5 text-red-500" />;
      default: return null;
    }
  };

  const getStatusText = (status: string) => {
    switch(status) {
      case 'validado': return 'Validado';
      case 'pendente': return 'Pendente';
      case 'invalido': return 'Inválido';
      default: return status;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Documentos</h1>
          <p className="text-gray-500">Gestão de documentos dos clientes</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={refresh}
            className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Atualizar
          </button>
          <label className="cursor-pointer">
            <input
              type="file"
              className="hidden"
              onChange={handleUpload}
              disabled={uploading || !clienteSelecionado}
              accept=".pdf,.jpg,.jpeg,.png"
            />
            <div className={`flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors ${uploading ? 'opacity-50 cursor-wait' : ''}`}>
              <Upload className="w-4 h-4" />
              {uploading ? 'Enviando...' : 'Upload'}
            </div>
          </label>
        </div>
      </div>

      {/* Dashboard de Validação */}
      {dashboard && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <p className="text-sm text-gray-500">Total de Documentos</p>
            <p className="text-2xl font-bold text-gray-900">{dashboard.estatisticas.total}</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <p className="text-sm text-gray-500">Pendentes</p>
            <p className="text-2xl font-bold text-yellow-600">{dashboard.estatisticas.pendentes}</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <p className="text-sm text-gray-500">Validados Hoje</p>
            <p className="text-2xl font-bold text-green-600">{dashboard.estatisticas.validados_hoje}</p>
          </div>
        </div>
      )}

      {/* Seletor de Cliente */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <select
          className="w-full md:w-96 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={clienteSelecionado}
          onChange={(e) => setClienteSelecionado(e.target.value)}
        >
          <option value="">Selecione um cliente</option>
          {clientes.map(c => (
            <option key={c.id} value={c.id}>{c.nome_completo}</option>
          ))}
        </select>
      </div>

      {/* Lista de Documentos */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        {loading && !documentos.length ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-500">Carregando documentos...</p>
          </div>
        ) : documentos.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>Nenhum documento encontrado</p>
            <p className="text-sm">Faça upload do primeiro documento</p>
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Documento</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Data</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Tipo</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Status</th>
                <th className="text-left px-6 py-3 text-sm font-medium text-gray-600">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {documentos.map((doc) => (
                <tr key={doc.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-900">{doc.nome}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {new Date(doc.data_upload).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{doc.tipo.toUpperCase()}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(doc.status)}
                      <span className={`text-sm ${
                        doc.status === 'validado' ? 'text-green-600' :
                        doc.status === 'pendente' ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {getStatusText(doc.status)}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleVisualizar(doc)}
                        className="p-1 hover:bg-gray-100 rounded transition-colors"
                        title="Visualizar"
                      >
                        <Eye className="w-4 h-4 text-gray-500" />
                      </button>
                      <button
                        onClick={() => handleDownload(doc)}
                        className="p-1 hover:bg-gray-100 rounded transition-colors"
                        title="Download"
                      >
                        <Download className="w-4 h-4 text-gray-500" />
                      </button>
                      {doc.status === 'pendente' && (
                        <>
                          <button
                            onClick={() => handleValidar(doc.id, 'validado')}
                            disabled={validando === doc.id}
                            className="p-1 hover:bg-green-100 rounded transition-colors"
                            title="Validar"
                          >
                            <CheckCircle className="w-4 h-4 text-green-500" />
                          </button>
                          <button
                            onClick={() => handleValidar(doc.id, 'invalido')}
                            disabled={validando === doc.id}
                            className="p-1 hover:bg-red-100 rounded transition-colors"
                            title="Rejeitar"
                          >
                            <XCircle className="w-4 h-4 text-red-500" />
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Documentos Pendentes */}
      {dashboard && dashboard.pendentes.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Documentos Pendentes</h2>
          <div className="space-y-2">
            {dashboard.pendentes.map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{doc.nome}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(doc.data_upload).toLocaleString('pt-BR')}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleValidar(doc.id, 'validado')}
                    disabled={validando === doc.id}
                    className="px-3 py-1 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors"
                  >
                    Validar
                  </button>
                  <button
                    onClick={() => handleValidar(doc.id, 'invalido')}
                    disabled={validando === doc.id}
                    className="px-3 py-1 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors"
                  >
                    Rejeitar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
