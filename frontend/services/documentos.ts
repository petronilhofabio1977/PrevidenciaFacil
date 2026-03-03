import api from './api';

export interface Documento {
  id: string;
  nome: string;
  tipo: string;
  status: 'pendente' | 'validado' | 'invalido' | 'em_analise';
  data_upload: string;
  tamanho: number;
  alertas?: string[];
  dados_extraidos?: any;
}

export interface DashboardValidacao {
  estatisticas: {
    total: number;
    pendentes: number;
    validados_hoje: number;
  };
  por_tipo: Array<{
    tipo: string;
    total: number;
  }>;
  pendentes: Array<{
    id: string;
    nome: string;
    tipo: string;
    data_upload: string;
    alertas: string[];
  }>;
}

export const documentosAPI = {
  // Upload de documento
  upload: async (clienteId: string, tipo: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('tipo', tipo);
    
    const response = await api.post(
      `/documentos/upload/${clienteId}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  // Listar documentos do cliente
  listarPorCliente: async (clienteId: string): Promise<Documento[]> => {
    const response = await api.get(`/documentos/cliente/${clienteId}`);
    return response.data;
  },

  // Dashboard de validação
  getDashboard: async (): Promise<DashboardValidacao> => {
    const response = await api.get('/documentos/dashboard/validacao');
    return response.data;
  },

  // Atualizar cadastro com dados extraídos
  atualizarCadastro: async (clienteId: string, documentoId: string) => {
    const response = await api.post(
      `/documentos/cliente/${clienteId}/atualizar-cadastro?documento_id=${documentoId}`
    );
    return response.data;
  },

  // Validar documento manualmente
  validarManual: async (documentoId: string, status: string, observacoes?: string) => {
    const response = await api.put(`/documentos/${documentoId}/validar`, {
      status,
      observacoes
    });
    return response.data;
  }
};
